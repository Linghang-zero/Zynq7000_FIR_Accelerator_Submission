"""Strict offline wrapper around the unchanged archived compare.py. Python 3.9+."""
import argparse,hashlib,json,math,re,struct,sys,types
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
def load_model():
    path=BASE/'scripts/compare.py'
    expected=json.loads((BASE/'references/provenance.json').read_text(encoding='utf-8'))
    if hashlib.sha256(path.read_bytes()).hexdigest()!=expected['compare_sha256']:
        raise ValueError('reference compare.py hash changed; model review required')
    m=types.ModuleType('archived_compare');m.__file__=str(path)
    exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__)
    return m,expected

def finite(values,label):
    if not all(math.isfinite(v) for v in values):raise ValueError(label+': non-finite values')

def verify(project,bin_path=None,signal=None,dump_path=None):
    m,prov=load_model();project=Path(project).resolve()
    hpath=project/'01_HLS_Accelerator/src/fir.cpp'
    ipath=project/'03_SDK_Software/fir_test/src/fir_test_inputs.h'
    text=m._strip_comments(hpath.read_text(encoding='utf-8'))
    # This package validates this fixed reference configuration, not arbitrary FIR types.
    for pattern in (r'typedef\s+ap_fixed\s*<\s*24\s*,\s*4\s*>\s*data_t',r'typedef\s+ap_fixed\s*<\s*24\s*,\s*2\s*>\s*coeff_t',r'typedef\s+ap_fixed\s*<\s*40\s*,\s*8\s*>\s*accum_t',r'typedef\s+ap_fixed\s*<\s*48\s*,\s*8\s*>\s*product_t'):
        if not re.search(pattern,text):raise ValueError('unsupported fixed-point configuration')
    h=m.parse_coeffs(hpath);inputs=m.parse_inputs(ipath)
    finite(h,'coefficients')
    if len(h)!=51 or h[0]!=0 or any(abs(h[k]-h[-1-k])>1e-9 for k in range(51)):
        raise ValueError('require 51 symmetric coefficients and h[0]=0')
    # Validate coefficients against the shipped source, while permitting whitespace/comment edits.
    expected_h=BASE/'references/coefficients.json'
    if h!=json.loads(expected_h.read_text(encoding='utf-8')):raise ValueError('coefficients changed; reference and thresholds must be revalidated')
    for name,x in inputs.items():
        finite(x,name)
        if len(x)!=1000:raise ValueError(name+': expected 1000 samples')
        if max(abs(v) for v in x)>=4:raise ValueError(name+': outside conservative supported input range abs(x)<4')
    mapping={'sine':inputs['SineInput'],'mixed':inputs['MixedInput'],'impulse':[1.0]+[0.0]*999}
    od=project/'04_Test_Evidence/output';dd=project/'04_Test_Evidence/dumps'
    if bin_path is not None:
        if signal not in mapping:raise ValueError('--bin requires --signal sine|mixed|impulse')
        targets=[(signal,Path(bin_path),Path(dump_path) if dump_path else None)]
    else:
        targets=[('sine',od/'fir_sine_fpga_1000.bin',dd/'sine_dump.txt'),
                 ('mixed',od/'fir_mixed_fpga_1000.bin',dd/'mixed_dump.txt'),
                 ('sine',od/'fir_sine_fpga_perf_1000.bin',None),
                 ('mixed',od/'fir_mixed_fpga_perf_1000.bin',dd/'mixed_dump_clean.txt'),
                 ('impulse',od/'fir_impulse_fpga_1000.bin',None)]
    results=[]
    for label,path,dump in targets:
        raw=path.read_bytes()
        if len(raw)!=4000:raise ValueError(path.name+': expected exactly 4000 bytes')
        y=m.read_bin(path);finite(y,path.name)
        ref=m.reference_fir(mapping[label],h)
        if len(y)!=len(ref):raise ValueError('reference/output sample count mismatch')
        errors=[abs(a-b) for a,b in zip(ref,y)]
        mx=max(errors);rmse=math.sqrt(sum(e*e for e in errors)/1000)
        match=None
        if dump is not None:
            vals=m.read_dump(dump);finite(vals,dump.name)
            if len(vals)!=1000:raise ValueError(dump.name+': expected exactly 1000 words')
            match=struct.pack('<1000f',*vals)==raw
        passed=mx<=3e-6 and sum(e>0.001 for e in errors)==0 and match is not False
        results.append({'case':label,'file':path.name,'samples':len(y),'bytes':len(raw),
                        'sha256':hashlib.sha256(raw).hexdigest(),'max_abs_error':mx,'rmse':rmse,
                        'points_gt_0.001':sum(e>0.001 for e in errors),'dump_equal':match,
                        'result':'PASS' if passed else 'FAIL'})
    return {'scope':'offline only; approximate quantized reference, not bit-accurate ap_fixed simulation',
            'endianness':'little; BIN has no self-describing byte order',
            'model_sha256':prov['compare_sha256'],'cases':results,
            'result':'PASS' if all(x['result']=='PASS' for x in results) else 'FAIL'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project',type=Path,default=BASE.parent)
    p.add_argument('--bin',type=Path);p.add_argument('--signal',choices=['sine','mixed','impulse'])
    p.add_argument('--dump',type=Path);p.add_argument('--output',type=Path)
    a=p.parse_args()
    if (a.signal or a.dump) and not a.bin:p.error('--signal/--dump require --bin')
    if a.output and a.output.exists():p.error('output exists; choose a new filename')
    try:
        result=verify(a.project,a.bin,a.signal,a.dump)
    except (OSError,ValueError,RuntimeError,OverflowError,struct.error) as e:
        result={'result':'ERROR','message':str(e)}
    payload=json.dumps(result,ensure_ascii=True,indent=2)
    if a.output:
        # Do not use this flag for existing source/data files. Exclusive create never overwrites.
        with a.output.open('x',encoding='utf-8') as f:f.write(payload+'\n')
    print(payload)
    return 0 if result['result']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
