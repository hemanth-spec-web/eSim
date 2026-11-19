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
| 8 | install-eSim-25.04.sh `copyKicadLibrary` | eSim's symbol table was copied to `~/.config/kicad/6.0` and the release template refers to `${KICAD6_SYMBOL_DIR}`; KiCad 8 reads `~/.config/kicad/8.0` and defines only `KICAD8_SYMBOL_DIR`, so a search for `eSim` in the symbol chooser returned nothing (21,700 default symbols loaded, 0 eSim) | Use the installed KiCad version for the folder and the variable name; after the fix `eSim_C`, `eSim_Diode`, `eSim_NPN` ... are listed | 3c36747b |
| 9 | uninstall path | Called the nghdl dispatcher (no 25.04 case), `llvm_version` was never set (purged `llvm-`), and it removed the hard-coded `kicad/6.0` | Use `install-nghdl-25.04.sh --uninstall`, set `llvm_version=18`, remove the folder of the installed KiCad version. **Not run** (it removes KiCad); checked with `bash -n` and review only | 902d1dbc |

Notes: the zip extracts install-eSim.sh without the execute bit (INSTALL already says chmod +x).
Logs: see logs/ (run1 = unmodified package, run2/3 = patched).

Observations, not fixed (outside the installer):
- eSim prints `QTextBrowser: No document for file:///.../src/browser/library/browser/welcome.html`; the file exists at `library/browser/welcome.html` in the zip, so the app looks in the wrong path. The Welcome pane is blank.
- `*** BUG *** In pixman_region32_init_rect: Invalid rectangle passed` is printed when eeschema opens in the VirtualBox guest; it did not stop the editor.
- On first start KiCad 8 asks to configure the global symbol library table (before fix 8 the eSim libraries are not in it).
