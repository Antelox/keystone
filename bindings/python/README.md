Keystone is a lightweight multi-platform, multi-architecture assembler framework.
It offers some unparalleled features:

- Multi-architecture, with support for Arm, Arm64 (AArch64/Armv8), Hexagon, Mips, PowerPC, Sparc, SystemZ & X86 (include
  16/32/64bit).
- Clean/simple/lightweight/intuitive architecture-neutral API.
- Implemented in C/C++ languages, with bindings for Python, NodeJS, Ruby, Go, Rust, Haskell & OCaml available.
- Native support for Windows & \*nix (with Mac OSX, Linux, *BSD & Solaris confirmed).
- Thread-safe by design.
- Open source - with a dual license.

Further information is available at http://www.keystone-engine.org

[License]

Keystone is available under a dual license:

- Version 2 of the GNU General Public License (GPLv2). (I.e. Without the "any later version" clause.).
  License information can be found in the COPYING and the EXCEPTIONS-CLIENT.

  This combination allows almost all the open source projects to use Keystone without conflicts.

- For commercial usage in production environments, contact the authors of Keystone to buy a royalty-free license.

  See LICENSE-COM.TXT for more information.

To install Python binding from Pypi (binary), simply do:

        pip install keystone-engine

In case you want to install from source code, follow the below steps.

0. Install the core engine as dependency

   Follow README.md in the root directory to compile & install the core.


1. To install pure Python binding on *nix, run the command below in the Python bindings directory:

        $ sudo make install

To install Python3 binding package, run the command below:
(Note: this requires python3 installed in your machine)

        $ sudo make install3

For example how to use Keystone API, see sample.py

2. To install Python binding on Windows:

Run the following command in command prompt:

        C:\> C:\location_to_python\python.exe setup.py install

Next, copy all the DLL files from the 'Core engine for Windows' package available
on the same Keystone download page and paste it in the path:

        C:\location_to_python\Lib\site-packages\keystone\
