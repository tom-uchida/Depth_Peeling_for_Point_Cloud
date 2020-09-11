===================================
          SPBR 
 (Stochastic Point-based Renderer)
    Installation manual 

       July 12, 2016
 Satoshi Tanaka and Kyoko Hasegawa
　　 Ritsumeikan University, Japan
　　     
Contact Address: stanaka@media.ritsumei.ac.jp
===================================

------------------------
0. What is SPBR? 
------------------------

 SPBR is a software application, in which we have implemented 
 our stochastic pointe-based rendering method. 
 SPBR enables quick and precise 3D see-through (transparent) 
 visualization of large-scale point clouds.

 SPBR is free software, which is licensed according to 
 GNU General Public License GPLv3: 
 https://www.gnu.org/licenses/gpl-3.0.en.html

 You can dawnload SPBR from the following GITHub site:
 https://github.com/stanakarits/SPBR
  
 For details on the rendering method, see the following 
 reference published by ourselves:

   S. Tanaka, K. Hasegawa, N. Okamoto, R. Umegaki, 
   S. Wang, M. Uemura, A. Okamoto, and K. Koyamada, 
   "See-Through Imaging of Laser-scanned 3D Cultural Heritage 
    Objects based on Stochastic Rendering of Large-Scale 
    Point Clouds", 
   ISPRS Ann. Photogramm. Remote Sens. Spatial Inf. Sci., 
   III-5, 73-80, doi:10.5194/isprs-annals-III-5-73-2016, 2016  
   (Proc. XXIII ISPRS Congress, July 12-19, 2016, Prague, Czech; 
    full paper accepted for oral presentation)


-----------------------------------------------
1. How to set up environments for installing SPBR
-----------------------------------------------

  You need to install GLEW and KVS (Kyoto Visualization System) before 
  installing SPBR.  You can download them from the following Web sites.
 
    GLEW: http://glew.sourceforge.net 
    KVS : https://github.com/naohisas/KVS

  Note: Install GLEW first and then install KVS.


--------------------------------------------------------------------
2. How to build, install, test (and uninstall) SPBR 
--------------------------------------------------------------------

  (0) Go to the directory spbr_VERSION/, which is created when 
     decompressing spbr_VERSION.tgz:
     Example) 
       $ cd spbr_VERSION/
       ("$" means the command prompt of your terminal application.)

  (1) Edit macro "INSTALL_DIR" in Makefile, if necessary.
      The default value is $(HOME)/local/bin:

        INSTALL_DIR=$(HOME)/local/bin 
   
      where $(HOME) indicates your home directory.
      The installation directory is automatically created if not exists.

      The two SPBR executable files (see (2)) will be 
      installed into the directory specified by the macro. 
      The command path should be set to the directory properly 
      (Edit ".bashrc", ".cshrc", etc in your home directory).

  (2) Build: 
        $ sh config_spbr.sh
        $ make clean 
        $ make 

      Note 2: This builds the following two executable files:
            spbr: stochastic point-based renderer (transparent rendering)
            opbr: opaque point-based renderer (opaque rendering)
 
  (3) Install:

      $ make install

    This copies the built executable files, "spbr" and "opbr", 
    into the directory by macro "INSTALL_DIR" (see (1) above). 

  Note:  
    Executing (2) + (3) is equivalent to "make autoinstall".


-----------
3. Test 
-----------
 USAGE : spbr file1.spbr file2.spbr ...

  $ spbr  ./SPBR_DATA/bunny05M.spbr
  $ spbr  ./SPBR_DATA/bunny05Mbin.spbr
  $ spbr  ./SPBR_DATA/bunny100k.spbr  ./SPBR_DATA/bunny100k_shift.spbr 
  $ spbr  ./SPBR_DATA/bunny100kbin.spbr  ./SPBR_DATA/bunny100kbin_shift.spbr 

  $ opbr  ./SPBR_DATA/bunny05M.spbr
  $ opbr  ./SPBR_DATA/bunny05Mbin.spbr
  $ opbr  ./SPBR_DATA/bunny100k.spbr  ./SPBR_DATA/bunny100k_shift.spbr 
  $ opbr  ./SPBR_DATA/bunny100kbin.spbr  ./SPBR_DATA/bunny100kbin_shift.spbr 

 KEYBOARD MENU:
  o-key: object control, l-key: light control
  s-key: snapshot image (BMP)
  S-key: snapshot image (PPM)
  G-key: snapshot image (PGM)
  q-key: quit


-----------
3. Help 
-----------

 The SPBR commands and the data format are displayed 
 by the "-h" option:

   $ spbr -h  | less 
   $ opbr -h  | less 

 See also spbr_data_format.txt in this directory.

-------------------------
4. Uninstallation
-------------------------

  $ make uninstall


---------------------
5. Node added
---------------------

* Application "SPBR Converter" (assumed name), 
  which can convert PLY files, XYZ files, etc. 
  to the SPBR files, shall be made public soon.
  This software will also support conversion from 
  an ASCII-format SPBR file to a binary-format SPBR file.

* Temporarily, you can use ../TOOL/CONVERT2BINARY 
  to convert an ASCII-format SPBR file to a binary-format 
  SPBR file. For details, see ../TOOL/README.txt.

// end of README.txt


