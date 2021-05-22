set root=C:\Users\jeongseokoon\anaconda3

call %root%\Scripts\activate.bat %root%

call conda activate py36
call cd C:\Users\jeongseokoon\projects\ARoMI\socket_codes
call python chatbot_client.py
pause
