{
  description = "async exaroton api wrapper";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts/";
    nix-systems.url = "github:nix-systems/default";
    starrpkgs = {
      url = "github:StarrFox/packages";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        flake-parts.follows = "flake-parts";
        nix-systems.follows = "nix-systems";
      };
    };
  };

  outputs = inputs @ {
    self,
    flake-parts,
    nix-systems,
    starrpkgs,
    ...
  }:
    flake-parts.lib.mkFlake {inherit inputs;} {
      debug = true;
      systems = import nix-systems;
      perSystem = {
        pkgs,
        system,
        self',
        ...
      }: let
        spkgs = starrpkgs.packages.${system};
        packageName = "exapy";
      in {
        devShells.default = pkgs.mkShell {
          name = packageName;
          packages = with pkgs; [
            poetry
            spkgs.commitizen
            just
            alejandra
            black
            isort
            python3Packages.vulture
          ];
        };
      };
    };
}
