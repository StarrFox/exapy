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

        customOverrides = self: super: {
          # looks like this:
          # uwuify = super.uwuify.overridePythonAttrs (
          #   old: {
          #     buildInputs = (old.buildInputs or []) ++ [super.poetry];
          #   }
          # );
        };

        packageName = "exapy";
      in {
        packages.${packageName} = pkgs.poetry2nix.mkPoetryApplication {
          projectDir = ./.;
          preferWheels = true;
          overrides = [
            pkgs.poetry2nix.defaultPoetryOverrides
            customOverrides
          ];
        };

        packages.default = self'.packages.${packageName};

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
