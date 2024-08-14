# $ nix-shell --pure
#
# Requires to have nix installed or using NixOS.
# 
{ pkgs ? import <nixpkgs> { } }:

let
  my-python = pkgs.python3;
  python-package-set = my-python.withPackages (p: with p; [
    black
    httpx
    isort
    poetry-core
    pytest
    rich
    ruff
    twine
    typer
    validators
  ]
  );
in
pkgs.mkShell {
  buildInputs = [
    pkgs.git
    pkgs.poetry
    python-package-set
  ];

  shellHook = ''
    export USERNAME=""
    export PASSWORD=""
    export URL=""
    PYTHONPATH=${python-package-set}/${python-package-set.sitePackages}
  '';
}
