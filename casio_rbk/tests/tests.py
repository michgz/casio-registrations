import unittest
from tempfile import gettempdir
import shutil
import os
import os.path
import filecmp
import struct

from casio_rbk.casio_rbk import RegistrationBank, Atom, Part
from casio_rbk.patch_name import patch_name


class TestCasioRbk(unittest.TestCase):
  
  def setUpClass():
    shutil.copyfile(os.path.join(os.path.dirname(__file__), "CT-X700 Testing Bank.RBK"), os.path.join(gettempdir(), "Test_01_Input.RBK"))
    shutil.copyfile(os.path.join(os.path.dirname(__file__), "CT-X700 Testing Bank.RBK"), os.path.join(gettempdir(), "Test_02_Input_Output.RBK"))
    shutil.copyfile(os.path.join(os.path.dirname(__file__), "CT-X700 Testing Bank.RBK"), os.path.join(gettempdir(), "Test_03_Input_Output.RBK"))
    shutil.copyfile(os.path.join(os.path.dirname(__file__), "CT-X3000 Testing Bank.RBK"), os.path.join(gettempdir(), "Test_04_Input.RBK"))
    shutil.copyfile(os.path.join(os.path.dirname(__file__), "CT-X700 Testing Bank.RBK"), os.path.join(gettempdir(), "Test_05_Input.RBK"))
    shutil.copyfile(os.path.join(os.path.dirname(__file__), "CT-X700 Testing Bank.RBK"), os.path.join(gettempdir(), "Test_06_Input_Output.RBK"))

  def tearDownClass():
    os.remove(os.path.join(gettempdir(), "Test_01_Input.RBK"))
    os.remove(os.path.join(gettempdir(), "Test_01_Output.RBK"))
    os.remove(os.path.join(gettempdir(), "Test_02_Input_Output.RBK"))
    os.remove(os.path.join(gettempdir(), "Test_03_Input_Output.RBK"))
    os.remove(os.path.join(gettempdir(), "Test_04_Input.RBK"))
    os.remove(os.path.join(gettempdir(), "Test_05_Input.RBK"))
    os.remove(os.path.join(gettempdir(), "Test_05_Output_1.txt"))
    os.remove(os.path.join(gettempdir(), "Test_05_Output_2.txt"))
    pass

    
  def test_01(self):
    # Just test reading and writing while making no changes
    #
    with open(os.path.join(gettempdir(), "Test_01_Input.RBK"), "rb") as f1:
      r = RegistrationBank.readFile(f1)
      
    self.assertEqual(len(r), 4)
    
    with open(os.path.join(gettempdir(), "Test_01_Output.RBK"), "wb") as f2:
      r.writeFile(f2)
    
    self.assertTrue(filecmp.cmp(os.path.join(gettempdir(), "Test_01_Output.RBK"), os.path.join(os.path.dirname(__file__), "Test_01_Expected_Output.RBK")))

  def test_02(self):
    # Reading/writing to the same file while making no changes
    #
    with open(os.path.join(gettempdir(), "Test_02_Input_Output.RBK"), "r+b") as f1:
      r = RegistrationBank.readFile(f1)
      r.writeFile(f1)
      self.assertEqual(len(r), 4)
    
    self.assertTrue(filecmp.cmp(os.path.join(gettempdir(), "Test_02_Input_Output.RBK"), os.path.join(os.path.dirname(__file__), "Test_02_Expected_Output.RBK")))
    
    
  def test_03(self):
    # Reading/writing to the same file while making some changes
    #
    with open(os.path.join(gettempdir(), "Test_03_Input_Output.RBK"), "r+b") as f1:
      r = RegistrationBank.readFile(f1)
      r[3].setVolumes(124, 125, 126)
      r[2].setPans(61, 62, 63)
      r.writeFile(f1)
      self.assertEqual(len(r), 4)
    
    self.assertTrue(filecmp.cmp(os.path.join(gettempdir(), "Test_03_Input_Output.RBK"), os.path.join(os.path.dirname(__file__), "Test_03_Expected_Output.RBK")))

  def test_04(self):
    # Check reading of 8-registration bank. Also check iteration over registrations
    #
    with open(os.path.join(gettempdir(), "Test_04_Input.RBK"), "rb") as f1:
      r = RegistrationBank.readFile(f1)
      self.assertEqual(len(r), 8)
      for rr in r:
        self.assertEqual(len(rr), 78)

  def test_05(self):
    # Check decoding of patch names.
    #
    with open(os.path.join(gettempdir(), "Test_05_Input.RBK"), "rb") as f1:
      r = RegistrationBank.readFile(f1)

    # Read patch names using the "convenience function"
    with open(os.path.join(gettempdir(), "Test_05_Output_1.txt"), "w") as f2:
      for i in range(5):
        f2.write(patch_name(*r[0].getPatchBank(i)) + "\n")

    # Read patch names using the full syntax -- result should be identical
    with open(os.path.join(gettempdir(), "Test_05_Output_2.txt"), "w") as f2:
      for i in range(5):
        f2.write(patch_name(*struct.unpack_from('<2B', r[0][Atom.Patch], 2*i)) + "\n")
      
    self.assertTrue(filecmp.cmp(os.path.join(gettempdir(), "Test_05_Output_1.txt"), os.path.join(os.path.dirname(__file__), "Test_05_Expected_Output.txt")))
    self.assertTrue(filecmp.cmp(os.path.join(gettempdir(), "Test_05_Output_2.txt"), os.path.join(os.path.dirname(__file__), "Test_05_Expected_Output.txt")))

  def test_06(self):
    # Check the example given in documentation
    with open(os.path.join(gettempdir(), "Test_06_Input_Output.RBK"), "r+b") as f1:
      r = RegistrationBank.readFile(f1)
      MyReg = r[0]
      
      vols = bytearray(MyReg[Atom.Volume])
      vols[Part.U2] = 115
      MyReg[Atom.Volume] = bytes(vols)
      
      r.writeFile(f1)
    
    self.assertTrue(filecmp.cmp(os.path.join(gettempdir(), "Test_06_Input_Output.RBK"), os.path.join(os.path.dirname(__file__), "Test_06_Expected_Output.RBK")))





if __name__=="__main__":
  unittest.main()
