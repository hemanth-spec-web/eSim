# eSim 2.5 on Ubuntu 25.04: installer issues and fixes

Environment: Ubuntu 25.04 (plucky) in VirtualBox, fresh install, Nov 2026. Package: eSim-2.5.zip.

| # | Where | Problem | Fix | Commit |
|---|---|---|---|---|
| 1 | Ubuntu/install-eSim.sh (installers branch) | Syntax error near `}`: merge 52d77f6d left an unclosed `if` and orphaned config lines | Closed the if block, removed orphaned lines | de342b7a |
| 2 | install-eSim.sh | FULL_VERSION empty on 25.04 (regex needed x.y.z) | Patch version made optional | 3bc948f5 |
| 3 | eSim-2.5 package | No 25.04 case or install-eSim-25.04.sh: "Unsupported Ubuntu version: 25.04 ()" | Not our change: upstream already added the 25.04 case and script on installers (f4cede1a); verified they work with the 2.5 package after fixes 1 and 2 | f4cede1a (upstream) |
| 4 | nghdl.zip dispatcher | No 25.04 case | install-nghdl-25.04.sh, copied in after unzip | 88d11ce4 |
| 5 | NGHDL (GTK) | libcanberra-gtk-module has no installation candidate on 25.04 | Install only libcanberra-gtk3-module | 88d11ce4 |
| 6 | GHDL 4.1.0 configure | "Unhandled version llvm 20.1.2" (accepts up to 18.1) | Use llvm-18 and llvm-config-18 | 88d11ce4 |
| 7 | NGHDL installNGHDL | mv fails ("Directory not empty") if ~/nghdl-simulator exists, so the install cannot be re-run | rm -rf before mv | 88d11ce4 |

Notes: the zip extracts install-eSim.sh without the execute bit (INSTALL already says chmod +x).
Logs: see logs/ (run1 = unmodified package, run2/3 = patched).
