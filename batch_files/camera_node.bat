set root=C:\Users\jeongseokoon\anaconda3

call %root%\Scripts\activate.bat %root%

call conda activate py36
call cd ../socket_codes
call python camera_node.py
pause
