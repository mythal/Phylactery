(use-modules (gnu packages python)
             (gnu packages python-xyz)
             (gnu packages protobuf)
             (pkgs cli-apps)
             (guix build-system python)
             (guix download)
             (guix profiles)
             (guix packages)
             ((guix licenses)
              #:prefix license:))

(define pkgs
  (list just poetry))

(packages->manifest pkgs)
