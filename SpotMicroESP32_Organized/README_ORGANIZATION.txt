SpotMicroESP32 - Organized print set
=====================================
Consolidated from the 3-part "SpotMicroESP32 (prints without supports)"
download (thing:4559827) + reinforced-shoulder remix (thing:4937631).
Categories + quantities verified against the official assembly guide:
https://github.com/michaelkubina/SpotMicroESP32/tree/master/assembly

IMPORTANT CORRECTION
--------------------
The four "shoulder" blocks (Bottom/Inner/Outer/Top_Shoulder) are CHASSIS parts,
printed 2x each - NOT leg parts and NOT 4x. They now live in Body/PLA_Black/.
The "Shoulder JOINT" parts (Servomount / Servo Cap / Ball Bearing Pin / Cover)
ARE leg parts (4x) and stay in Leg/.

PRINT QUANTITIES
================
LEG/  (one leg's worth; x4 total. "mirror" = print 2 as-is + 2 mirrored L/R)
  PLA_Black:
    Wrist ......................... 4x (mirror)
    Wrist__Counterpart ............ 4x (mirror)
    Limb_Top_Shell_with_BB_hole ... 4x (mirror)
    Limb_Bottom_Shell ............. 4x (mirror)
    Limb_Servohorn_Mount_long_v4 .. 4x (mirror)
    Limb_Ball_Bearing_Mount_long_v4 4x (mirror)
    Shoulder_Joint_Servomount_extended_BB . 4x (mirror)
    Shoulder_Joint_Servo_Cap_Extended ..... 4x
    Shoulder_Joint_Ball_Bearing_Pin_M3x8 .. 4x
  PLA_Blue:
    Shoulder_Cover ................ 4x
  TPU:
    Foot_Tip ...................... 4x

BODY/  (chassis + hull + head; 1x unless noted)
  PLA_Black:
    Bottom_Shoulder ............... 2x   <- moved here (chassis)
    Inner_Shoulder ................ 2x   <- moved here (chassis)
    Outer_Shoulder ................ 2x   <- moved here (chassis)
    Top_Shoulder .................. 2x   <- moved here (chassis)
    Chassis_Side .................. 2x
    Circuitry_Mountingplate_* ..... 1x  (print only the pair for YOUR converter:
                                        XL4016 or SZBK07)
    LiPo_Mountingbracket_F/M/R .... 1x each
    cameramount_esp32_cam ......... 1x
    cameramount_esp32_cam_counterpiece  1x
    sensormount_esp32_cam ......... 1x
    TTL_Counterpiece .............. 1x
  PLA_Blue (covers):
    Top_Cover_Split_Front/Rear .... 1x each
    Bottom_Cover_Split_Front/Rear . 1x each
    Front_Cover_Optimized ......... 1x
    Rear cover: pick ONE set -
      long : Rear_Cover_Shell_Long + Rear_Cover_Plate
      medium (remix): Rear_Cover_Shell_Medium + Rear_Cover_Plate_Medium
    Template files = editable bases, not printed directly.

HEADS-UP: BALL BEARING PIN (not yet resolved)
---------------------------------------------
The assembly guide uses the SAME "Shoulder Joint Ball Bearing Pin" in TWO
places: 4x at the knees/wrists AND 4x at the shoulder joints (8x total).
The reinforced remix only replaced the SHOULDER-JOINT pin (the _M3x8 version
now in Leg/). The 4x pins for the KNEES still use the original stock pin, which
is currently sitting in Leg/_stock_versions_replaced_by_remix/. Don't delete
that folder - you still need that pin x4 for the wrists.

BALL BEARINGS: 8x 625ZZ for the base build (4 knees + 4 shoulder joints).

Nothing was deleted. Original three part-folders are untouched.
