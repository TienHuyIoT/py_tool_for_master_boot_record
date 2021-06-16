Source tree production tools WatchMe

├── Guideline_release.txt
├── build_dfu_encrypt_firmware.py 
├── build_mainHeader.py
├── config
│   └── config.json
├── gen_release
│   ├── app
│   │   ├── build_mainHeader.bat
│   │   └── main_app.hex                    <------- main_app.hex (main application)
│   ├── boot
│   ├── final
│   │   ├── main_app_dfu.bin                <------- dfu encrypt file
│   │   └── mbr_main_release.hex            <------- release file for production
│   ├── mbr
│   │   └── mbr.hex                         <------- mbr.hex (master boot record)
│   └── scripts
│       ├── 01_gen_image_release.bat        <------- run this script to generate mbr_main_release.hex and main_app_dfu.bin file
│       ├── 02_jlink_program_release.bat    <------- run this script to program mbr_main_release.hex to device by j-link command
│       ├── 03_jlink_erase_chip.bat
│       ├── 04_jlink_program_mbr.bat
│       ├── 05_jlink_read_entire_chip.bat
│       └── jlink_scripts
│           ├── erase.jlink
│           ├── nrf52840.jflash
│           ├── read.jlink
│           ├── write.jlink
│           └── write_mbr.jlink
├───helpers
│   └───__pycache__
└───utils
    └───__pycache__

1. software setup 
- Python3 or latest version.
  Link: https://www.python.org/downloads/
- NRF command line Tools (build in nrf-connect).
  Link: https://www.nordicsemi.com/Software-and-tools/Development-Tools/nRF-Command-Line-Tools/Download
- J-Link.
  Link: https://www.segger.com/downloads/jlink/#J-LinkSoftwareAndDocumentationPack

2. Edit config\config.json
    {					 
        "input_binary": "C:/04 Project/01. Xoontec/01_WatchMe/ProductionToolsWatchMe/gen_release/app/main_app.bin",
        "output_file":  "C:/04 Project/01. Xoontec/01_WatchMe/ProductionToolsWatchMe/gen_release/final/main_app_dfu.bin",
        "output_mainHeader_file":  "C:/04 Project/01. Xoontec/01_WatchMe/ProductionToolsWatchMe/gen_release/app/mainHeader.bin",
        "fw_type": "0x55010000",
        "fw_type_dfu": "0x55010101",
        "fw_version": "0x00010003",
        "aes-key": "9a950f6c4fa1f919cb1e1539564723e2",
        "aes-iv-length": 16,
        "aes-iv": "45c4250f8d7985a1e74692c7dd247983"
    }

    Explains :
        - "input_binary": path to main application input
        - "output_file": path to save main application dfu output
        - "output_mainHeader_file": path to save mainHeader output
        - "fw_type": 55(signal)-00/01(boot/app firmware)-00/01(raw/encrypt firmware)-00/01(internal/external memory location)
            "fw_type": "0x55010000",     /* 55(signal)-01(app)-00(raw image)-00(internal) */
            "fw_type_dfu": "0x55010101", /* 55(signal)-01(app)-01(encrypt)-01(external) */
        - "fw_version": 0xAABBCCCC       /* AA: major, BB: minor, CCCC: build*/
            "fw_version": "0x00010002",  /* v0.1.2 */
        - "aes-key": key AES128
        - "aes-iv": iv AES128
        - "aes-iv-length": length AES128

3. Edit gen_release\app\build_mainHeader.bat
    Edit path to convert bin2hex by using J-Flash

    - Edit path stored mainHeader.bin from json config file above
        mainApp_path="C:\04 Project\01. Xoontec\01_WatchMe\ProductionToolsWatchMe\gen_release\app"
    - Edit path j-flash setup
        jlink_path="C:\Program Files (x86)\SEGGER\JLink"

    **************** Note ****************
    0x15FE0 is address store mainHeader (16-Byte) to MBR update at the first start application.
    set mainHeader_start_addr=0x15FE0
    set mainHeader_stop_addr=0x15FF0

    0x61000 is start address of main application using for j-flash tool convert hex2bin
    set mainApp_start_addr=0x61000
    set mainApp_stop_addr=0x100000
    *************** End Note *************

4. Edit gen_release\scripts\01_gen_image_release.bat
    script_path="C:\04 Project\01. Xoontec\01_WatchMe\ProductionToolsWatchMe\gen_release\scripts"

5. Gen release and dfu image
    - Run file 01_gen_image_release.bat in gen_release\scripts folder
    - mbr_main_release.hex and main_app_dfu.bin in gen_release\final folder

    **** If get error, pls install package missing for python. ****

6. Program mbr_main_release.hex
    - Edit 02_jlink_program_release.bat in gen_release\scripts folder
        set file="C:\04 Project\01. Xoontec\01_WatchMe\ProductionToolsWatchMe\gen_release\scripts\jlink_scripts\write.jlink"
        cd /d "C:\Program Files (x86)\SEGGER\JLink"

    - Edit write.jlink in gen_release\scripts\jlink_scripts folder
        loadfile "C:\04 Project\01. Xoontec\01_WatchMe\ProductionToolsWatchMe\gen_release\final\mbr_main_release.hex", 0

    - Run 02_jlink_program_release.bat in gen_release\scripts folder
    If get error, retry it again.
