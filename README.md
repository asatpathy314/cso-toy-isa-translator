# cso-toy-isa-translator
Translator that takes in hex commands and converts it to understandable instructions in the UVA CS 2130 Toy Instruction Set Architecture (ISA).

No need to install any external libraries.

Example Usage:

```python
from translator import program_translator

converter = Translator("file_path_to_your_hex_file")
print(converter.readable)
```

