"""Regression and deliberately corrupted offline fixtures; no hardware operations."""
import contextlib,io,json,shutil,struct,subprocess,sys,tempfile,unittest
from pathlib import Path
import verify_fir as v

class VerifyTests(unittest.TestCase):
    project=Path(__file__).resolve().parents[2]
    def test_original_reference_main(self):
        m,_=v.load_model();m.INPUT_H=self.project/'03_SDK_Software/fir_test/src/fir_test_inputs.h'
        m.FIR_CPP=self.project/'01_HLS_Accelerator/src/fir.cpp'
        m.OUT_DIR=self.project/'04_Test_Evidence/output';m.DUMP_DIR=self.project/'04_Test_Evidence/dumps'
        with contextlib.redirect_stdout(io.StringIO()) as stream:self.assertEqual(m.main(),0)
        self.assertIn('fir_impulse_fpga_1000.bin',stream.getvalue())
    def test_input_length_and_amplitude(self):
        with tempfile.TemporaryDirectory(prefix='fir_skill_test_') as td:
            root=Path(td)
            for rel in ['01_HLS_Accelerator/src/fir.cpp','03_SDK_Software/fir_test/src/fir_test_inputs.h']:
                (root/rel).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(self.project/rel,root/rel)
            header=root/'03_SDK_Software/fir_test/src/fir_test_inputs.h'
            for count,value in [(999,'0.0f'),(1000,'4.0f')]:
                header.write_text('static const float SineInput[] = {'+','.join([value]*count)+'};\nstatic const float MixedInput[] = {'+','.join(['0.0f']*1000)+'};')
                with self.assertRaises(ValueError):v.verify(root)
    def test_archived_five_cases(self):
        r=v.verify(self.project);self.assertEqual(r['result'],'PASS');self.assertEqual(len(r['cases']),5)
        self.assertEqual(sum(c['dump_equal'] is True for c in r['cases']),3)
    def test_reject_corrupt_inputs(self):
        raw=(self.project/'04_Test_Evidence/output/fir_sine_fpga_perf_1000.bin').read_bytes()
        with tempfile.TemporaryDirectory(prefix='fir_skill_test_') as td:
            p=Path(td)/'negative.bin'
            for data in (b'',raw[:-4],raw+b'xxxx',struct.pack('<f',float('nan'))+raw[4:]):
                p.write_bytes(data)
                with self.assertRaises(ValueError):v.verify(self.project,p,'sine')
    def test_reject_mismatch_and_byte_swap(self):
        with tempfile.TemporaryDirectory(prefix='fir_skill_test_') as td:
            p=Path(td)/'negative.bin'
            raw=(self.project/'04_Test_Evidence/output/fir_sine_fpga_perf_1000.bin').read_bytes()
            p.write_bytes(b''.join(raw[i:i+4][::-1] for i in range(0,4000,4)))
            try:self.assertEqual(v.verify(self.project,p,'sine')['result'],'FAIL')
            except ValueError:pass # non-finite byte-swapped words are also correctly rejected
            p.write_bytes(raw)
            self.assertEqual(v.verify(self.project,p,'mixed')['result'],'FAIL')
            bad=Path(td)/'dump.txt';bad.write_text('00000000\n'*1000)
            self.assertEqual(v.verify(self.project,p,'sine',bad)['result'],'FAIL')
    def test_missing_file(self):
        with self.assertRaises(OSError):v.verify(self.project,self.project/'not_a_real_output.bin','sine')
    def test_coefficient_and_type_guard(self):
        with tempfile.TemporaryDirectory(prefix='fir_skill_test_') as td:
            root=Path(td)
            for rel in ['01_HLS_Accelerator/src/fir.cpp','03_SDK_Software/fir_test/src/fir_test_inputs.h']:
                (root/rel).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(self.project/rel,root/rel)
            f=root/'01_HLS_Accelerator/src/fir.cpp';text=f.read_text()
            for altered in [text.replace('ap_fixed<24, 4>','ap_fixed<25, 4>'),text.replace('0.04737780','0.04700000')]:
                f.write_text(altered)
                with self.assertRaises(ValueError):v.verify(root)
    def test_cli_exit_and_exclusive_output(self):
        script=Path(v.__file__)
        with tempfile.TemporaryDirectory(prefix='fir_skill_test_') as td:
            output=Path(td)/'result.json';cmd=[sys.executable,'-B',str(script),'--project',str(self.project),'--output',str(output)]
            first=subprocess.run(cmd,capture_output=True);self.assertEqual(first.returncode,0)
            before=output.read_bytes();self.assertEqual(json.loads(before)['result'],'PASS')
            again=subprocess.run(cmd,capture_output=True);self.assertNotEqual(again.returncode,0);self.assertEqual(output.read_bytes(),before)
if __name__=='__main__':unittest.main(verbosity=2)
