import os
import sys
import io
import unittest

from vcstools.vcs_base import VcsClientBase, VcsError, sanitized, normalized_rel_path, run_shell_command

class SvnClientTestSetups(unittest.TestCase):

      def test_normalized_rel_path(self):
            self.assertEqual(None, normalized_rel_path(None, None))
            self.assertEqual('foo', normalized_rel_path(None, 'foo'))
            self.assertEqual('/foo', normalized_rel_path(None, '/foo'))
            self.assertEqual('../bar', normalized_rel_path('/bar', '/foo'))
            self.assertEqual('../bar', normalized_rel_path('/bar', '/foo/baz/..'))
            self.assertEqual('../bar', normalized_rel_path('/bar/bam/foo/../..', '/foo/baz/..'))
            self.assertEqual('bar', normalized_rel_path('bar/bam/foo/../..', '/foo/baz/..'))

      def test_sanitized(self):
            self.assertEqual('', sanitized(None))
            self.assertEqual('', sanitized(''))
            self.assertEqual('"foo"', sanitized('foo'))
            self.assertEqual('"foo"', sanitized('\"foo\"'))
            self.assertEqual('"foo"', sanitized('"foo"'))
            self.assertEqual('"foo"', sanitized('" foo"'))

            try:
                  sanitized('bla"; foo"')
                  self.fail("Expected Exception")
            except VcsError:
                  pass
            try:
                  sanitized('bla";foo"')
                  self.fail("Expected Exception")
            except VcsError:
                  pass
            try:
                  sanitized('bla";foo \"bum')
                  self.fail("Expected Exception")
            except VcsError:
                  pass
            try:
                  sanitized('bla";foo;"bam')
                  self.fail("Expected Exception")
            except VcsError:
                  pass
            try:
                  sanitized('bla"#;foo;"bam')
                  self.fail("Expected Exception")
            except VcsError:
                  pass

      def test_shell_command(self):
            self.assertEqual((0, "", None), run_shell_command("true"))
            self.assertEqual((1, "", None), run_shell_command("false"))
            self.assertEqual((0, "foo", None), run_shell_command("echo foo", shell = True))
            (v, r, e ) = run_shell_command("[", shell = True)
            self.assertFalse(v == 0)
            self.assertFalse(e is None)
            self.assertEqual(r, '')
            (v, r, e ) = run_shell_command("echo foo && [", shell = True)
            self.assertFalse(v == 0)
            self.assertFalse(e is None)
            self.assertEqual(r, 'foo')
            # not a great test on a system where this is default
            self.assertEqual((0, "LANG=en_US.UTF-8", None), run_shell_command("/usr/bin/env |grep LANG", shell = True, us_env = True))
            try:
                  run_shell_command("two words")
                  self.fail("expected exception")
            except: pass
