{ pkgs ? import <nixpkgs> {} }:
let
  python-with-packages = pkgs.python3.withPackages (p: with p; [
    grpcio
  ]);
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    python-with-packages
    poetry
    just
    dprint
  ];
  shellHook = ''
    PYTHONPATH=${python-with-packages}/${python-with-packages.sitePackages}
  '';
}
