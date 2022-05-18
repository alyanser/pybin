simple wrapper over nasm and objdump

requirements:
python3, nasm & objdump

usage:
-h | --help -> show help
-a | --arch -> specify architecture for nasm
-n | --no-interactive -> do not print instructions interactively

examples:

	./pybin.py -n
	nop
	xor eax, eax
	int 0x80

output:

	--------------------------------------------------
	90
	--------------------------------------------------
	0x90
	--------------------------------------------------
	\x90
	--------------------------------------------------
	{ '\x90' }

	--------------------------------------------------
	31 c0
	--------------------------------------------------
	0x310xc0
	--------------------------------------------------
	\x31\xc0
	--------------------------------------------------
	{ '\x31', '\xc0' }

	--------------------------------------------------
	cd 80
	--------------------------------------------------
	0xcd0x80
	--------------------------------------------------
	\xcd\x80
	--------------------------------------------------
	{ '\xcd', '\x80' }

	--------------------------------------------------
	90 31 c0 cd 80
	--------------------------------------------------
	0x900x310xc00xcd0x80
	--------------------------------------------------
	\x90\x31\xc0\xcd\x80
	--------------------------------------------------
	{ '\x90', '\x31', '\xc0', '\xcd', '\x80' }

