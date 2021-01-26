EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 1 1
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
L Connector:Conn_01x02_Male J1
U 1 1 5D8FF802
P 5000 3950
F 0 "J1" H 5108 4131 50  0000 C CNN
F 1 "Conn_01x02_Male" H 5108 4040 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Horizontal" H 5000 3950 50  0001 C CNN
F 3 "~" H 5000 3950 50  0001 C CNN
	1    5000 3950
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J2
U 1 1 5D9007E0
P 5950 3800
F 0 "J2" H 6030 3842 50  0000 L CNN
F 1 "Conn_01x01" H 6030 3751 50  0000 L CNN
F 2 "SMD_Packages:1Pin" H 5950 3800 50  0001 C CNN
F 3 "~" H 5950 3800 50  0001 C CNN
	1    5950 3800
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J3
U 1 1 5D900D08
P 5950 4200
F 0 "J3" H 6030 4242 50  0000 L CNN
F 1 "Conn_01x01" H 6030 4151 50  0000 L CNN
F 2 "SMD_Packages:1Pin" H 5950 4200 50  0001 C CNN
F 3 "~" H 5950 4200 50  0001 C CNN
	1    5950 4200
	1    0    0    -1  
$EndComp
Wire Wire Line
	5200 3950 5500 3950
Wire Wire Line
	5500 3950 5500 3800
Wire Wire Line
	5500 3800 5750 3800
Wire Wire Line
	5200 4050 5500 4050
Wire Wire Line
	5500 4050 5500 4200
Wire Wire Line
	5500 4200 5750 4200
$EndSCHEMATC
