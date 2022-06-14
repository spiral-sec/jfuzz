# jfuzz

Simple CAN fuzzer on the terminal

Supports Linux using the `can-utils` package, and the CAN kernel module, and Windows with Vector's 
[Canalyzer](https://www.vector.com/fr/fr/produits/produits-a-z/software/canalyzer/)

## Features

- Pulls CAN messages and Signals from a [dbc](https://github.com/stefanhoelzl/CANpy) file
- Randomizes signals inside CAN message and absolutely blast the CAN bus with them
- BLF Logging on Windows

> This project is still under development, more features are coming but any help is welcome !

## Installing
```bash
python -m venv
. venv/bin/activate
pip install -r requirements.txt
```

## Run on Windows

1. Plug your Vector License (I used a [VN 7610](https://www.vector.com/fr/fr/produits/produits-a-z/hardware/network-interfaces/vn7610/)
but other Vector-supported hardware should work as well) on your computer
2. Open `Vector Hardware Manager` and make sure your connector register `CANalyzer` on the first channel
3. Drop your `.dbc` file(s) in the current directory
4. `. venv/bin/activate && python main.py`

## Run on Linux

1. Open another terminal in the `scripts/` directory
2. Run `./vcan.sh -i` to install and setup your `vcan0` controller thingy
3. drop your `.dbc` file(s) in the current directory
4. run `./vcan.sh -m [your file].dbc` to monitor `vcan0` with your database
5. `. venv/bin/activate && python main.py`