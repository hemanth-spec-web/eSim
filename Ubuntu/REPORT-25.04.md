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
| 9 | uninstall path | Called the nghdl dispatcher (no 25.04 case), `llvm_version` was never set (the purge command is built with an empty version), and it removed the hard-coded `kicad/6.0` | Use `install-nghdl-25.04.sh --uninstall`, set `llvm_version=18`, remove the folder of the installed KiCad version. Run on the clean install (logs/uninstall-test.log): ends with "eSim Uninstalled Successfully"; afterwards `/usr/bin/esim`, `~/.esim`, `/usr/share/kicad`, the SKY130 PDK, `~/nghdl-simulator` and the desktop icon are gone and no kicad package is installed | 902d1dbc |
| 10 | `copyKicadLibrary` (template `sym-lib-table`) | The template lists 28 `Legacy` `.lib` libraries (abm, analog, CONNECT, LTspice_*, ...) whose files the package does not install into `/usr/share/kicad/symbols`; KiCad 8 shows a "Load Error" listing them the first time the symbol chooser opens (seen on the clean run) | Entries whose file is missing are marked `(disabled)` after the table is written; script check (logs/check-symtable.py): enabled-but-missing 28 -> 0, eSim entries still 15 | fc2d7b05 |

Notes: the zip extracts install-eSim.sh without the execute bit (INSTALL already says chmod +x).
Logs (in logs/): run1-unmodified-package.log = unpatched eSim-2.5 package (stops with "Unsupported Ubuntu version: 25.04 ()"); run2.log = first run with the patched scripts (stops in NGHDL); nghdl-manual*.log = NGHDL installer run on its own while fixing it; run3-resume.log = last two steps (SKY130, launcher); run4-clean.log = full install from a clean snapshot with the final scripts.

Observations, not fixed (outside the installer):
- eSim prints `QTextBrowser: No document for file:///.../src/browser/library/browser/welcome.html`; the file exists at `library/browser/welcome.html` in the zip, so the app looks in the wrong path. The Welcome pane is blank.
- `*** BUG *** In pixman_region32_init_rect: Invalid rectangle passed` is printed when eeschema opens in the VirtualBox guest; it did not stop the editor.
- Before fix 8, KiCad 8's first start asked to configure the global symbol library table and the eSim libraries were missing from it. After fix 8 only KiCad 8's "Configure Global Footprint Library Table" prompt remains (the package ships no footprint table).

## Methodology
- Test machine: fresh Ubuntu 25.04 VM (VirtualBox) with snapshots, so every attempt starts from a known state; every run logged with `tee`.
- Issue 1: `./install-eSim.sh --help` failed with a syntax error. `bash -n` over every commit that touched the file showed that only merge 52d77f6d is broken; `git diff` against the previous commit showed the missing `else`/`fi`.
- Issues 2-3: ran the unmodified eSim-2.5 package ("Unsupported Ubuntu version: 25.04 ()"), then compared its dispatcher and the 24.04/25.04 scripts with `diff`.
- Issues 4-7: ran the NGHDL installer on its own with logging, one failure at a time; the LLVM fix was checked with a 2-minute `configure` run before starting the hour-long build.
- Issues 8 and 10: opened the schematic editor and searched the symbol chooser; compared the symbol library table with the files on disk with a short script.
- Issue 9 (uninstall): read and syntax-checked, then run on the installed system and checked with `ls` and `dpkg`.
- Final check: full install from a clean snapshot (run4-clean.log), then eSim and the symbol chooser.

## Verification
Clean run: VM restored to a fresh Ubuntu 25.04 snapshot, eSim-2.5.zip (sha256 in logs/eSim-2.5.zip.sha256) plus the three scripts from this branch, then `./install-eSim.sh --install`. `logs/run4-clean.log` ends with "eSim Installed Successfully". eSim starts, and the symbol chooser lists the eSim libraries (see screenshots/).

Not covered by that run: fix 10 was tested on the `copyKicadLibrary` function alone and then in the GUI (no Load Error when the symbol chooser was opened); the KiCad 8 first-run "Configure Global Footprint Library Table" dialog is not addressed (the package ships no footprint table).

Second clean run (run5): VM restored again to the same fresh snapshot, same checksum-verified eSim-2.5.zip, final scripts from this branch (including fix 10). `logs/run5-clean.log` (25,514 lines) ends with "eSim Installed Successfully"; GHDL 4.1.0, Verilator 4.210 and ngspice-35 are installed; `~/.config/kicad` contains only `8.0`; `logs/check-symtable.py` reports `enabled-but-missing: 0  eSim entries: 15`; opening the symbol chooser shows no Load Error and lists the eSim libraries (720 symbols loaded, screenshots/run5-chooser-eSim-libraries.png). So fix 10 is verified from a clean install, not only by the function test.

Screenshots:
- screenshots/issue1-broken-if-block-1.png : issue 1: the unclosed if block in install-eSim.sh
- screenshots/issue1-broken-if-block-2.png : issue 1: the same function, continued
- screenshots/issue1-merge-diff.png : issue 1: diff of merge 52d77f6d
- screenshots/clean-run-install-success.png : clean run: installer finished
- screenshots/issue10-load-error.png : issue 10: Load Error for missing legacy libraries
- screenshots/kicad8-footprint-table-dialog.png : KiCad 8 first-run footprint table prompt
- screenshots/issue8-fixed-eSim-libraries-in-chooser.png : issue 8: eSim libraries in the symbol chooser after the fix
- screenshots/run5-chooser-eSim-libraries.png : run5: symbol chooser on a clean install, eSim libraries listed, no Load Error
