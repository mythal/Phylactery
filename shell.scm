(use-modules (gnu packages python)
             (gnu packages python-web)
             (gnu packages python-xyz)
             (gnu packages protobuf)
             (gnu packages rpc)
             (pkgs cli-apps)
             (guix build-system python)
             (guix download)
             (guix profiles)
             (guix packages)
             ((guix licenses)
              #:prefix license:))

(define python-googleapis-common-protos-x
  (package
    (name "python-googleapis-common-protos")
    (version "1.56.4")
    (source (origin
              (method url-fetch)
              (uri (pypi-uri "googleapis-common-protos" version))
              (sha256
               (base32
                "05s4dszqd5pjwjh4bdic40v1v447k0a3dynsrgypqf3rfb276n62"))))
    (build-system python-build-system)
    (propagated-inputs (list python-protobuf-x))
    (home-page "https://github.com/googleapis/python-api-common-protos")
    (synopsis "Common protobufs used in Google APIs")
    (description "Common protobufs used in Google APIs")
    (license #f)))

(define python-google-api-core-x
  (package
    (name "python-google-api-core")
    (version "2.10.2")
    (source (origin
              (method url-fetch)
              (uri (pypi-uri "google-api-core" version))
              (sha256
               (base32
                "080kjwmih8ij389xcb1ryr5ng953w7l7acsjhwgphmzy75vnzh0h"))))
    (build-system python-build-system)
    (propagated-inputs (list python-google-auth
                             python-googleapis-common-protos-x
                             python-protobuf-x python-requests))
    (arguments
     `(#:tests? #f))
    (home-page "https://github.com/googleapis/python-api-core")
    (synopsis "Google API client core library")
    (description "Google API client core library")
    (license license:asl2.0)))

(define python-proto-plus-x
  (package
    (name "python-proto-plus")
    (version "1.22.1")
    (source (origin
              (method url-fetch)
              (uri (pypi-uri "proto-plus" version))
              (sha256
               (base32
                "1ym2wf5xi3ah3dhyjzvqp85windiypj6nx2lysgh3y7y5l9gszbc"))))
    (build-system python-build-system)
    (propagated-inputs (list python-protobuf-x))
    (native-inputs (list python-google-api-core-x))
    (home-page "https://github.com/googleapis/proto-plus-python.git")
    (synopsis "Beautiful, Pythonic protocol buffers.")
    (description "Beautiful, Pythonic protocol buffers.")
    (license license:asl2.0)))

(define python-protobuf-x
  (package
    (name "python-protobuf")
    (version "4.21.7")
    (source (origin
              (method url-fetch)
              (uri (pypi-uri "protobuf" version))
              (sha256
               (base32
                "0mw7digwnrh1nr7k997k3jh0wjq33sjjw7l0ia3jqhyk7shdpnbi"))))
    (build-system python-build-system)
    (home-page "https://developers.google.com/protocol-buffers/")
    (synopsis "")
    (description "")
    (license #f)))

(define python-futures-x
  (package
    (name "python-futures")
    (version "3.3.0")
    (source (origin
              (method url-fetch)
              (uri (pypi-uri "futures" version))
              (sha256
               (base32
                "154pvaybk9ncyb1wpcnzgd7ayvvhhzk92ynsas7gadaydbvkl0vy"))))
    (build-system python-build-system)
    (home-page "https://github.com/agronholm/pythonfutures")
    (synopsis "Backport of the concurrent.futures package from Python 3")
    (description "Backport of the concurrent.futures package from Python 3")
    (license #f)))

(define python-grpcio-x
  (package
    (inherit python-grpcio)
    (name "python-grpcio")
    (version "1.49.1")
    (source (origin
              (method url-fetch)
              (uri (pypi-uri "grpcio" version))
              (sha256
               (base32
                "17y9lm1nsmfcf3lksi63zfkim2a6ampv4sz2da82524fxk4mywnl"))
              (modules '((guix build utils)
                         (ice-9 ftw)))
              (snippet '(begin
                          (with-directory-excursion "third_party"
                            (for-each delete-file-recursively
                                      (scandir "."
                                               (lambda (file)
                                                 (not (member file
                                                              '("." ".."
                                                                "address_sorting"
                                                                "upb" "xxhash")))))))))))))

(define python-grpcio-status-x
  (package
    (name "python-grpcio-status")
    (version "1.49.1")
    (source (origin
              (method url-fetch)
              (uri (pypi-uri "grpcio-status" version))
              (sha256
               (base32
                "1ngmrjx0sxb83psmy0r0gir00p6lw1s2sc5xxsvcgq3f2kf4i3v5"))))
    (build-system python-build-system)
    (arguments
     `(#:tests? #f))
    (propagated-inputs (list python-googleapis-common-protos-x python-grpcio-x
                             python-protobuf-x))
    (home-page "https://grpc.io")
    (synopsis "Status proto mapping for gRPC")
    (description "Status proto mapping for gRPC")
    (license #f)))

(define python-google-cloud-compute-x
  (package
    (name "python-google-cloud-compute")
    (version "1.6.1")
    (source (origin
              (method url-fetch)
              (uri (pypi-uri "google-cloud-compute" version))
              (sha256
               (base32
                "0w04jsijxk1wa8kfifg9v68ihgwwn9jbhch88xljzhs967ykvy16"))))
    (build-system python-build-system)
    (arguments
     `(#:tests? #f))
    (propagated-inputs (list python-google-api-core-x python-proto-plus-x
                             python-protobuf-x python-grpcio-x
                             python-grpcio-status-x))
    (home-page "https://github.com/googleapis/python-compute")
    (synopsis "")
    (description "")
    (license license:asl2.0)))

(define pkgs
  (list python python-google-api-core-x python-google-cloud-compute-x
        python-flask just))

(packages->manifest pkgs)
