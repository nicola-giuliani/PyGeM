from unittest import TestCase
import unittest
import pygem.utils as ut
import pygem.params as pars
import numpy as np
import filecmp
import os
import vtk


class TestUtils(TestCase):
    def cmp(self, f1, f2):
        """
        Check if the two files have the same content, skipping comment lines
        """
        content1 = [line for line in open(f1) if not line.startswith('#')]
        content2 = [line for line in open(f1) if not line.startswith('#')]
        return content1 == content2

    def test_utils_write_original_box(self):
        params = pars.FFDParameters()
        params.read_parameters(
            filename='tests/test_datasets/parameters_test_ffd_sphere.prm')

        outfilename = 'tests/test_datasets/box_test_sphere.vtk'

        ut.write_bounding_box(params, outfilename, write_deformed=False)
        os.remove(outfilename)

    def test_utils_write_modified_box(self):
        params = pars.FFDParameters()
        params.read_parameters(
            filename='tests/test_datasets/parameters_test_ffd_sphere.prm')

        outfilename = 'tests/test_datasets/box_test_sphere.vtk'

        ut.write_bounding_box(params, outfilename)
        os.remove(outfilename)

    def test_utils_check_vtk_original_box(self):
        params = pars.FFDParameters()
        params.read_parameters(
            filename='tests/test_datasets/parameters_test_ffd_sphere.prm')

        outfilename = 'tests/test_datasets/box_test_sphere.vtk'
        if vtk.VTK_MAJOR_VERSION <= 5:
            outfilename_expected = 'tests/test_datasets/box_test_sphere_true_version5.vtk'
        else:
            outfilename_expected = 'tests/test_datasets/box_test_sphere_true_version6.vtk'

        ut.write_bounding_box(params, outfilename, write_deformed=False)

        self.assertTrue(self.cmp(outfilename, outfilename_expected))
        os.remove(outfilename)

    def test_utils_check_vtk_modified_box(self):
        params = pars.FFDParameters()
        params.read_parameters(
            filename='tests/test_datasets/parameters_test_ffd_sphere.prm')

        outfilename = 'tests/test_datasets/box_test_sphere.vtk'
        if vtk.VTK_MAJOR_VERSION <= 5:
            outfilename_expected = 'tests/test_datasets/box_modified_test_sphere_true_version5.vtk'
        else:
            outfilename_expected = 'tests/test_datasets/box_modified_test_sphere_true_version6.vtk'

        ut.write_bounding_box(params, outfilename)

        self.assertTrue(self.cmp(outfilename, outfilename_expected))
        os.remove(outfilename)

    def test_utils_plot_rbf_control_points(self):
        params = pars.RBFParameters()
        params.read_parameters(
            filename='tests/test_datasets/parameters_rbf_cube.prm')
        ut.plot_rbf_control_points(params, save_fig=False)

    def test_utils_plot_rbf_control_points_save_fig(self):
        params = pars.RBFParameters()
        params.read_parameters(
            filename='tests/test_datasets/parameters_rbf_cube.prm')
        ut.plot_rbf_control_points(params, save_fig=True)
        self.assertTrue(os.path.isfile('RBF_control_points.png'))
        os.remove('RBF_control_points.png')

    def test_utils_check_write_points_in_vtp(self):
        ctrl_points = np.arange(12).reshape(4, 3)

        outfilename = 'tests/test_datasets/points_test.vtp'
        if vtk.VTK_MAJOR_VERSION >= 6:
            outfilename_expected = 'tests/test_datasets/points_test_true_version6.vtp'

        ut.write_points_in_vtp(ctrl_points, outfile=outfilename)
        self.assertTrue(self.cmp(outfilename, outfilename_expected))
        os.remove(outfilename)
