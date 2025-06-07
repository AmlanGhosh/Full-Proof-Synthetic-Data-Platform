{ pkgs }: {
  deps = [
    pkgs.lsof
    pkgs.bashInteractive
    pkgs.nodePackages.bash-language-server
    pkgs.man
  ];
}