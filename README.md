# checker-game
เกมหมากฮอส (Checkers) เป็นเกมกระดานสำหรับสองคนที่มีการเล่นบนกระดานสี่เหลี่ยมขนาด 8x8 ผู้เล่นจะควบคุมหมากของตัวเองและพยายามที่จะกำจัดหมากของคู่ต่อสู้โดยการกระโดดข้าม

# ระบบภายในเกม
- การเคลื่อนที่ของหมากตามกฎหมากฮอส
- ระบบการเซฟและโหลดเกม
- การตรวจสอบผู้ชนะ
- การเน้นหมากที่สามารถเคลื่อนที่ได้
- การเน้นการจับหมากคู่ต่อสู้

# แนะนำการติดตั้ง
1. ติดตั้ง Python (แนะนำ Python 3.6 ขึ้นไป)
2. ติดตั้งไลบรารี Tkinter หากยังไม่มี

# รายละเอียดของโค้ด
โค้ดนี้ใช้ Tkinter สำหรับการสร้าง GUI โดยมีฟังก์ชันการทำงานหลักดังนี้
__init__ : สร้างหน้าต่างเกมและกำหนดค่าต่างๆ
create_board : สร้างกระดานหมากฮอส
place_pieces : วางหมากในตำแหน่งเริ่มต้น
on_click : จัดการการคลิกของผู้เล่น
highlight_piece : ไฮไลท์หมากที่ถูกเลือกเพื่อให้ผู้เล่นดูง่าย
highlight_available_moves : ไฮไลท์ตำแหน่งที่สามารถเคลื่อนที่ได้เพื่อให้ผู้เล่นดูง่าย
end_turn : เปลี่ยนเทิร์นผู้เล่น
save_game : เซฟสถานะเกมในไฟล์
load_game : โหลดสถานะเกมจากไฟล์
