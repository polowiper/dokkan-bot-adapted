{
  description = "A python devshell containing all the dependencies required to run this bot";

  inputs.nixpkgs.url = "nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs, ... }:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs {
      inherit system;
    };
  in {
    devShells.${system}.default = pkgs.mkShell {
      packages = with pkgs; [
        python311
        python311Packages.pyinstaller
        python311Packages.colorama
        python311Packages.pycryptodome
        python311Packages.cython
#        python311Packages.pysimplegui
        python311Packages.peewee
        python311Packages.requests

      ];
      shellHook = ''
        echo "Python devShell"
      '';
    };
  };
}
