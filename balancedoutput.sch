EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:switches
LIBS:relays
LIBS:motors
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:pcm2900
LIBS:xlr4
LIBS:AudioMapperUSB-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 2 2
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L XLR4BODYPIN J15
U 1 1 6057A0F8
P 3750 2300
F 0 "J15" H 3900 2550 50  0000 C CNN
F 1 "XLR4BODYPIN" H 3500 2550 50  0000 C CNN
F 2 "AudioMapperUSB:IOXLR3MEH" H 3750 2300 50  0001 C CNN
F 3 "" H 3750 2300 50  0001 C CNN
	1    3750 2300
	-1   0    0    -1  
$EndComp
Text GLabel 1400 1200 0    60   Input ~ 0
VBUS
$Comp
L CP_Small C29
U 1 1 6057BDC8
P 1450 1500
F 0 "C29" H 1460 1570 50  0000 L CNN
F 1 "10 uF" V 1300 1450 50  0000 L CNN
F 2 "AudioMapperUSB:CP_1206_HandSoldering" H 1450 1500 50  0001 C CNN
F 3 "" H 1450 1500 50  0001 C CNN
F 4 " C7171" H 1450 1500 60  0001 C CNN "LCSC"
	1    1450 1500
	1    0    0    -1  
$EndComp
$Comp
L C_Small C35
U 1 1 6057BDD0
P 1850 1500
F 0 "C35" H 1860 1570 50  0000 L CNN
F 1 "1 uF" V 2000 1400 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 1850 1500 50  0001 C CNN
F 3 "" H 1850 1500 50  0001 C CNN
F 4 "C28323" H 1850 1500 60  0001 C CNN "LCSC"
	1    1850 1500
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR41
U 1 1 6057BDD7
P 1650 1650
F 0 "#PWR41" H 1650 1400 50  0001 C CNN
F 1 "GND" H 1650 1500 50  0000 C CNN
F 2 "" H 1650 1650 50  0001 C CNN
F 3 "" H 1650 1650 50  0001 C CNN
	1    1650 1650
	1    0    0    -1  
$EndComp
$Comp
L LM358 U9
U 1 1 6057BE27
P 2650 1600
F 0 "U9" H 2650 1800 50  0000 L CNN
F 1 "OPA2170" H 2650 1400 50  0000 L CNN
F 2 "Housings_SOIC:SOIC-8_3.9x4.9mm_Pitch1.27mm" H 2650 1600 50  0001 C CNN
F 3 "" H 2650 1600 50  0001 C CNN
F 4 "C56285" H 2650 1600 60  0001 C CNN "LCSC"
	1    2650 1600
	1    0    0    -1  
$EndComp
Text GLabel 1450 2100 0    60   Input ~ 0
LEFTCH
$Comp
L GND #PWR43
U 1 1 60580E25
P 2550 2200
F 0 "#PWR43" H 2550 1950 50  0001 C CNN
F 1 "GND" H 2550 2050 50  0000 C CNN
F 2 "" H 2550 2200 50  0001 C CNN
F 3 "" H 2550 2200 50  0001 C CNN
	1    2550 2200
	1    0    0    -1  
$EndComp
$Comp
L LM358 U9
U 2 1 60580ECC
P 2650 2800
F 0 "U9" H 2650 3000 50  0000 L CNN
F 1 "OPA2170" H 2650 2600 50  0000 L CNN
F 2 "Housings_SOIC:SOIC-8_3.9x4.9mm_Pitch1.27mm" H 2650 2800 50  0001 C CNN
F 3 "" H 2650 2800 50  0001 C CNN
F 4 "C56285" H 2650 2800 60  0001 C CNN "LCSC"
	2    2650 2800
	1    0    0    -1  
$EndComp
$Comp
L R R40
U 1 1 60581C61
P 2100 2900
F 0 "R40" V 2180 2900 50  0000 C CNN
F 1 "10k" V 2100 2900 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 2030 2900 50  0001 C CNN
F 3 "" H 2100 2900 50  0001 C CNN
F 4 "C17414" V 2100 2900 60  0001 C CNN "LCSC"
	1    2100 2900
	0    1    1    0   
$EndComp
$Comp
L R R69
U 1 1 60581F21
P 2700 3350
F 0 "R69" V 2780 3350 50  0000 C CNN
F 1 "10k" V 2700 3350 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 2630 3350 50  0001 C CNN
F 3 "" H 2700 3350 50  0001 C CNN
F 4 "C17414" V 2700 3350 60  0001 C CNN "LCSC"
	1    2700 3350
	0    1    1    0   
$EndComp
Text GLabel 1350 2700 0    60   Input ~ 0
VCOM
$Comp
L GND #PWR46
U 1 1 6058250D
P 4250 2500
F 0 "#PWR46" H 4250 2250 50  0001 C CNN
F 1 "GND" H 4250 2350 50  0000 C CNN
F 2 "" H 4250 2500 50  0001 C CNN
F 3 "" H 4250 2500 50  0001 C CNN
	1    4250 2500
	1    0    0    -1  
$EndComp
$Comp
L R R70
U 1 1 60582617
P 3300 1750
F 0 "R70" V 3380 1750 50  0000 C CNN
F 1 "100R" V 3300 1750 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 3230 1750 50  0001 C CNN
F 3 "" H 3300 1750 50  0001 C CNN
F 4 "C17408" V 3300 1750 60  0001 C CNN "LCSC"
	1    3300 1750
	1    0    0    -1  
$EndComp
$Comp
L CP_Small C49
U 1 1 60582700
P 3300 2100
F 0 "C49" H 3310 2170 50  0000 L CNN
F 1 "10 uF" V 3150 2050 50  0000 L CNN
F 2 "AudioMapperUSB:CP_1206_HandSoldering" H 3300 2100 50  0001 C CNN
F 3 "" H 3300 2100 50  0001 C CNN
F 4 " C7171" H 3300 2100 60  0001 C CNN "LCSC"
	1    3300 2100
	-1   0    0    -1  
$EndComp
$Comp
L C_Small C32
U 1 1 60582A9F
P 1800 2850
F 0 "C32" H 1810 2920 50  0000 L CNN
F 1 "1 uF" V 1950 2750 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 1800 2850 50  0001 C CNN
F 3 "" H 1800 2850 50  0001 C CNN
F 4 "C28323" H 1800 2850 60  0001 C CNN "LCSC"
	1    1800 2850
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR42
U 1 1 60582D01
P 1800 3050
F 0 "#PWR42" H 1800 2800 50  0001 C CNN
F 1 "GND" H 1800 2900 50  0000 C CNN
F 2 "" H 1800 3050 50  0001 C CNN
F 3 "" H 1800 3050 50  0001 C CNN
	1    1800 3050
	1    0    0    -1  
$EndComp
$Comp
L R R34
U 1 1 60582E6B
P 1550 2700
F 0 "R34" V 1630 2700 50  0000 C CNN
F 1 "100R" V 1550 2700 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 1480 2700 50  0001 C CNN
F 3 "" H 1550 2700 50  0001 C CNN
F 4 "C17408" V 1550 2700 60  0001 C CNN "LCSC"
	1    1550 2700
	0    -1   -1   0   
$EndComp
Wire Wire Line
	1450 1600 1850 1600
Wire Wire Line
	1650 1650 1650 1600
Connection ~ 1650 1600
Wire Wire Line
	1450 1400 1850 1400
Wire Wire Line
	1650 1200 1650 1400
Connection ~ 1650 1400
Wire Wire Line
	2550 1200 2550 1300
Wire Wire Line
	2350 1700 2250 1700
Wire Wire Line
	2250 1700 2250 2500
Wire Wire Line
	2250 2100 3100 2100
Wire Wire Line
	3100 2100 3100 1600
Wire Wire Line
	1400 1200 2550 1200
Connection ~ 1650 1200
Wire Wire Line
	1450 2100 2000 2100
Wire Wire Line
	2000 2100 2000 1500
Wire Wire Line
	2000 1500 2350 1500
Wire Wire Line
	2550 2200 2550 1900
Wire Wire Line
	1950 2900 1950 2500
Wire Wire Line
	1950 2500 2250 2500
Connection ~ 2250 2100
Wire Wire Line
	2250 2900 2350 2900
Wire Wire Line
	2300 2900 2300 3350
Wire Wire Line
	2300 3350 2550 3350
Connection ~ 2300 2900
Wire Wire Line
	2950 2800 3100 2800
Wire Wire Line
	3100 2800 3100 3350
Wire Wire Line
	2850 3350 3300 3350
Connection ~ 3100 1600
Wire Wire Line
	1700 2700 2350 2700
Wire Wire Line
	1800 2750 1800 2700
Connection ~ 1800 2700
Wire Wire Line
	1800 3050 1800 2950
Wire Wire Line
	1400 2700 1350 2700
Wire Wire Line
	2950 1600 3300 1600
Wire Wire Line
	3300 2000 3300 1900
Wire Wire Line
	3300 2200 3300 2300
Wire Wire Line
	3300 2300 3400 2300
$Comp
L R R71
U 1 1 60583804
P 3300 3200
F 0 "R71" V 3380 3200 50  0000 C CNN
F 1 "100R" V 3300 3200 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 3230 3200 50  0001 C CNN
F 3 "" H 3300 3200 50  0001 C CNN
F 4 "C17408" V 3300 3200 60  0001 C CNN "LCSC"
	1    3300 3200
	1    0    0    -1  
$EndComp
$Comp
L CP_Small C50
U 1 1 605838E2
P 3300 2900
F 0 "C50" H 3310 2970 50  0000 L CNN
F 1 "10 uF" V 3150 2850 50  0000 L CNN
F 2 "AudioMapperUSB:CP_1206_HandSoldering" H 3300 2900 50  0001 C CNN
F 3 "" H 3300 2900 50  0001 C CNN
F 4 " C7171" H 3300 2900 60  0001 C CNN "LCSC"
	1    3300 2900
	1    0    0    1   
$EndComp
Connection ~ 3100 3350
Wire Wire Line
	3300 3050 3300 3000
Wire Wire Line
	3300 2800 3300 2650
Wire Wire Line
	3300 2650 3750 2650
Wire Wire Line
	4250 2300 4250 2500
Wire Wire Line
	4250 2300 4100 2300
Connection ~ 4250 2450
$Comp
L XLR4BODYPIN J22
U 1 1 605842E3
P 7550 2350
F 0 "J22" H 7700 2600 50  0000 C CNN
F 1 "XLR4BODYPIN" H 7300 2600 50  0000 C CNN
F 2 "AudioMapperUSB:IOXLR3MEH" H 7550 2350 50  0001 C CNN
F 3 "" H 7550 2350 50  0001 C CNN
	1    7550 2350
	-1   0    0    -1  
$EndComp
Text GLabel 5200 1250 0    60   Input ~ 0
VBUS
$Comp
L CP_Small C51
U 1 1 605842EB
P 5250 1550
F 0 "C51" H 5260 1620 50  0000 L CNN
F 1 "10 uF" V 5100 1500 50  0000 L CNN
F 2 "AudioMapperUSB:CP_1206_HandSoldering" H 5250 1550 50  0001 C CNN
F 3 "" H 5250 1550 50  0001 C CNN
F 4 " C7171" H 5250 1550 60  0001 C CNN "LCSC"
	1    5250 1550
	1    0    0    -1  
$EndComp
$Comp
L C_Small C53
U 1 1 605842F2
P 5650 1550
F 0 "C53" H 5660 1620 50  0000 L CNN
F 1 "1 uF" V 5800 1450 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 5650 1550 50  0001 C CNN
F 3 "" H 5650 1550 50  0001 C CNN
F 4 "C28323" H 5650 1550 60  0001 C CNN "LCSC"
	1    5650 1550
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR47
U 1 1 605842F8
P 5450 1700
F 0 "#PWR47" H 5450 1450 50  0001 C CNN
F 1 "GND" H 5450 1550 50  0000 C CNN
F 2 "" H 5450 1700 50  0001 C CNN
F 3 "" H 5450 1700 50  0001 C CNN
	1    5450 1700
	1    0    0    -1  
$EndComp
$Comp
L LM358 U10
U 1 1 605842FF
P 6450 1650
F 0 "U10" H 6450 1850 50  0000 L CNN
F 1 "OPA2170" H 6450 1450 50  0000 L CNN
F 2 "Housings_SOIC:SOIC-8_3.9x4.9mm_Pitch1.27mm" H 6450 1650 50  0001 C CNN
F 3 "" H 6450 1650 50  0001 C CNN
F 4 "C56285" H 6450 1650 60  0001 C CNN "LCSC"
	1    6450 1650
	1    0    0    -1  
$EndComp
Text GLabel 5250 2150 0    60   Input ~ 0
RIGHTCH
$Comp
L GND #PWR49
U 1 1 60584306
P 6350 2250
F 0 "#PWR49" H 6350 2000 50  0001 C CNN
F 1 "GND" H 6350 2100 50  0000 C CNN
F 2 "" H 6350 2250 50  0001 C CNN
F 3 "" H 6350 2250 50  0001 C CNN
	1    6350 2250
	1    0    0    -1  
$EndComp
$Comp
L LM358 U10
U 2 1 6058430D
P 6450 2850
F 0 "U10" H 6450 3050 50  0000 L CNN
F 1 "OPA2170" H 6450 2650 50  0000 L CNN
F 2 "Housings_SOIC:SOIC-8_3.9x4.9mm_Pitch1.27mm" H 6450 2850 50  0001 C CNN
F 3 "" H 6450 2850 50  0001 C CNN
F 4 "C56285" H 6450 2850 60  0001 C CNN "LCSC"
	2    6450 2850
	1    0    0    -1  
$EndComp
$Comp
L R R73
U 1 1 60584314
P 5900 2950
F 0 "R73" V 5980 2950 50  0000 C CNN
F 1 "10k" V 5900 2950 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 5830 2950 50  0001 C CNN
F 3 "" H 5900 2950 50  0001 C CNN
F 4 "C17414" V 5900 2950 60  0001 C CNN "LCSC"
	1    5900 2950
	0    1    1    0   
$EndComp
$Comp
L R R74
U 1 1 6058431B
P 6500 3400
F 0 "R74" V 6580 3400 50  0000 C CNN
F 1 "10k" V 6500 3400 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 6430 3400 50  0001 C CNN
F 3 "" H 6500 3400 50  0001 C CNN
F 4 "C17414" V 6500 3400 60  0001 C CNN "LCSC"
	1    6500 3400
	0    1    1    0   
$EndComp
Text GLabel 5150 2750 0    60   Input ~ 0
VCOM
$Comp
L GND #PWR52
U 1 1 60584322
P 8050 2550
F 0 "#PWR52" H 8050 2300 50  0001 C CNN
F 1 "GND" H 8050 2400 50  0000 C CNN
F 2 "" H 8050 2550 50  0001 C CNN
F 3 "" H 8050 2550 50  0001 C CNN
	1    8050 2550
	1    0    0    -1  
$EndComp
$Comp
L R R75
U 1 1 60584329
P 7100 1800
F 0 "R75" V 7180 1800 50  0000 C CNN
F 1 "100R" V 7100 1800 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 7030 1800 50  0001 C CNN
F 3 "" H 7100 1800 50  0001 C CNN
F 4 "C17408" V 7100 1800 60  0001 C CNN "LCSC"
	1    7100 1800
	1    0    0    -1  
$EndComp
$Comp
L CP_Small C54
U 1 1 60584330
P 7100 2150
F 0 "C54" H 7110 2220 50  0000 L CNN
F 1 "10 uF" V 6950 2100 50  0000 L CNN
F 2 "AudioMapperUSB:CP_1206_HandSoldering" H 7100 2150 50  0001 C CNN
F 3 "" H 7100 2150 50  0001 C CNN
F 4 " C7171" H 7100 2150 60  0001 C CNN "LCSC"
	1    7100 2150
	-1   0    0    -1  
$EndComp
$Comp
L C_Small C52
U 1 1 60584337
P 5600 2900
F 0 "C52" H 5610 2970 50  0000 L CNN
F 1 "1 uF" V 5750 2800 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 5600 2900 50  0001 C CNN
F 3 "" H 5600 2900 50  0001 C CNN
F 4 "C28323" H 5600 2900 60  0001 C CNN "LCSC"
	1    5600 2900
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR48
U 1 1 6058433D
P 5600 3100
F 0 "#PWR48" H 5600 2850 50  0001 C CNN
F 1 "GND" H 5600 2950 50  0000 C CNN
F 2 "" H 5600 3100 50  0001 C CNN
F 3 "" H 5600 3100 50  0001 C CNN
	1    5600 3100
	1    0    0    -1  
$EndComp
$Comp
L R R72
U 1 1 60584344
P 5350 2750
F 0 "R72" V 5430 2750 50  0000 C CNN
F 1 "100R" V 5350 2750 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 5280 2750 50  0001 C CNN
F 3 "" H 5350 2750 50  0001 C CNN
F 4 "C17408" V 5350 2750 60  0001 C CNN "LCSC"
	1    5350 2750
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5250 1650 5650 1650
Wire Wire Line
	5450 1700 5450 1650
Connection ~ 5450 1650
Wire Wire Line
	5250 1450 5650 1450
Wire Wire Line
	5450 1250 5450 1450
Connection ~ 5450 1450
Wire Wire Line
	6350 1250 6350 1350
Wire Wire Line
	6150 1750 6050 1750
Wire Wire Line
	6050 1750 6050 2550
Wire Wire Line
	6050 2150 6900 2150
Wire Wire Line
	6900 2150 6900 1650
Wire Wire Line
	5200 1250 6350 1250
Connection ~ 5450 1250
Wire Wire Line
	5250 2150 5800 2150
Wire Wire Line
	5800 2150 5800 1550
Wire Wire Line
	5800 1550 6150 1550
Wire Wire Line
	6350 2250 6350 1950
Wire Wire Line
	5750 2950 5750 2550
Wire Wire Line
	5750 2550 6050 2550
Connection ~ 6050 2150
Wire Wire Line
	6050 2950 6150 2950
Wire Wire Line
	6100 2950 6100 3400
Wire Wire Line
	6100 3400 6350 3400
Connection ~ 6100 2950
Wire Wire Line
	6750 2850 6900 2850
Wire Wire Line
	6900 2850 6900 3400
Wire Wire Line
	6650 3400 7100 3400
Connection ~ 6900 1650
Wire Wire Line
	5500 2750 6150 2750
Wire Wire Line
	5600 2800 5600 2750
Connection ~ 5600 2750
Wire Wire Line
	5600 3100 5600 3000
Wire Wire Line
	5200 2750 5150 2750
Wire Wire Line
	6750 1650 7100 1650
Wire Wire Line
	7100 2050 7100 1950
Wire Wire Line
	7100 2250 7100 2350
Wire Wire Line
	7100 2350 7200 2350
$Comp
L R R76
U 1 1 60584371
P 7100 3250
F 0 "R76" V 7180 3250 50  0000 C CNN
F 1 "100R" V 7100 3250 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 7030 3250 50  0001 C CNN
F 3 "" H 7100 3250 50  0001 C CNN
F 4 "C17408" V 7100 3250 60  0001 C CNN "LCSC"
	1    7100 3250
	1    0    0    -1  
$EndComp
$Comp
L CP_Small C55
U 1 1 60584378
P 7100 2950
F 0 "C55" H 7110 3020 50  0000 L CNN
F 1 "10 uF" V 6950 2900 50  0000 L CNN
F 2 "AudioMapperUSB:CP_1206_HandSoldering" H 7100 2950 50  0001 C CNN
F 3 "" H 7100 2950 50  0001 C CNN
F 4 " C7171" H 7100 2950 60  0001 C CNN "LCSC"
	1    7100 2950
	1    0    0    1   
$EndComp
Connection ~ 6900 3400
Wire Wire Line
	7100 3100 7100 3050
Wire Wire Line
	7100 2850 7100 2700
Wire Wire Line
	7100 2700 7550 2700
Wire Wire Line
	8050 2350 8050 2550
Wire Wire Line
	8050 2350 7900 2350
Connection ~ 8050 2500
$Comp
L R R78
U 1 1 60581BD5
P 3600 2900
F 0 "R78" V 3680 2900 50  0000 C CNN
F 1 "1M" V 3600 2900 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 3530 2900 50  0001 C CNN
F 3 "" H 3600 2900 50  0001 C CNN
F 4 "C17514" V 3600 2900 60  0001 C CNN "LCSC"
	1    3600 2900
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR45
U 1 1 60581DA3
P 3600 3100
F 0 "#PWR45" H 3600 2850 50  0001 C CNN
F 1 "GND" H 3600 2950 50  0000 C CNN
F 2 "" H 3600 3100 50  0001 C CNN
F 3 "" H 3600 3100 50  0001 C CNN
	1    3600 3100
	1    0    0    -1  
$EndComp
Wire Wire Line
	3600 3100 3600 3050
Wire Wire Line
	3600 2750 3600 2650
Connection ~ 3600 2650
$Comp
L R R77
U 1 1 60581F32
P 3150 2400
F 0 "R77" V 3230 2400 50  0000 C CNN
F 1 "1M" V 3150 2400 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 3080 2400 50  0001 C CNN
F 3 "" H 3150 2400 50  0001 C CNN
F 4 "C17514" V 3150 2400 60  0001 C CNN "LCSC"
	1    3150 2400
	-1   0    0    1   
$EndComp
Wire Wire Line
	3300 2250 3150 2250
Connection ~ 3300 2250
$Comp
L GND #PWR44
U 1 1 605820EB
P 3150 2600
F 0 "#PWR44" H 3150 2350 50  0001 C CNN
F 1 "GND" H 3150 2450 50  0000 C CNN
F 2 "" H 3150 2600 50  0001 C CNN
F 3 "" H 3150 2600 50  0001 C CNN
	1    3150 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	3150 2600 3150 2550
$Comp
L R R80
U 1 1 6058221B
P 7450 2950
F 0 "R80" V 7530 2950 50  0000 C CNN
F 1 "1M" V 7450 2950 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 7380 2950 50  0001 C CNN
F 3 "" H 7450 2950 50  0001 C CNN
F 4 "C17514" V 7450 2950 60  0001 C CNN "LCSC"
	1    7450 2950
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR51
U 1 1 605823B1
P 7450 3150
F 0 "#PWR51" H 7450 2900 50  0001 C CNN
F 1 "GND" H 7450 3000 50  0000 C CNN
F 2 "" H 7450 3150 50  0001 C CNN
F 3 "" H 7450 3150 50  0001 C CNN
	1    7450 3150
	1    0    0    -1  
$EndComp
Wire Wire Line
	7450 3150 7450 3100
Wire Wire Line
	7450 2800 7450 2700
Connection ~ 7450 2700
$Comp
L R R79
U 1 1 60582598
P 7000 2450
F 0 "R79" V 7080 2450 50  0000 C CNN
F 1 "1M" V 7000 2450 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 6930 2450 50  0001 C CNN
F 3 "" H 7000 2450 50  0001 C CNN
F 4 "C17514" V 7000 2450 60  0001 C CNN "LCSC"
	1    7000 2450
	-1   0    0    1   
$EndComp
Wire Wire Line
	7100 2300 7000 2300
Connection ~ 7100 2300
$Comp
L GND #PWR50
U 1 1 605826F7
P 7000 2650
F 0 "#PWR50" H 7000 2400 50  0001 C CNN
F 1 "GND" H 7000 2500 50  0000 C CNN
F 2 "" H 7000 2650 50  0001 C CNN
F 3 "" H 7000 2650 50  0001 C CNN
	1    7000 2650
	1    0    0    -1  
$EndComp
Wire Wire Line
	7000 2650 7000 2600
$EndSCHEMATC
