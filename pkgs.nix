let
  # Tracking nixos-unstable as of 2021-08-11.
  nixpkgsCommit = "6e287913f7b1ef537c97aa301b67c34ea46b640f";
  nixpkgsSrc = fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/${nixpkgsCommit}.tar.gz";
    sha256 = "sha256:1pydgwya807f2n74cd3ppxk6gyapk8v00rgz8jjh07zm4lxcmil0";
  };
  nixpkgs = import nixpkgsSrc {
    config.allowUnfree = true;
    config.allowBroken = true;
  };

in with nixpkgs; rec {
  # nixpkgs passthrough
  inherit (nixpkgs) pkgs lib;
  # All packages require to build/lint the project.
  midimacropadDev = [ python311 ] ++ (with python311Packages; [ mido ipython black ]);
}
