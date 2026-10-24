import sys, unittest
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/tests/')
s = unittest.defaultTestLoader.discover('/mnt/project-files/robot-cad/research/sldprt/tools/tests/', top_level_dir='/mnt/project-files/robot-cad/research/sldprt/tools/tests/')
r = unittest.TextTestRunner(verbosity=1).run(s)
sys.exit(not r.wasSuccessful())
