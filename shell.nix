with import ./pkgs.nix;
pkgs.mkShell {
  name = "midimacropad-shell";
  buildInputs = midimacropadDev ++ (with pkgs; []);
}
