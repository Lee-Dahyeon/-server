from flask import Flask, request #flask.py안에 Flask class 로드/ request: 요청 관련 클래스
from flask import render_template # html 로드하는 클래스
from werkzeug.utils import secure_filename # 파일 이름, 경로에 대한 기본적인 보안

# flask server 보안 규칙
# 1. html 문서들은 render_template으로 로드 시
# 반드시 template폴더 내에 존재해야 한다
# 2. 모든 경로에 대해 접근 불가
# 단, static경로만 접근 가능

import os

if not os.path.exists('static/imgs'): # ('static/imgs')폴더가 없으면 만들어라
    os.makedirs('static/imgs')


app=Flask(__name__)#__name__내장변수를 매개변수로 Flask 클래스에 담아 인스턴스 app생성(생성된 인스턴스 app에 저장)

@app.route('/') #IPv4:port + '/' 경로 접속 시 호출되는 함수 정의
def index():
    # return 쓸 수 있는 결과는 html
    # 1. 태그를 직접 
    # 2. 라이브러리 render_template 이용
    
    return '''
    <!- HTML문서를 직접 만들자-!>
    <style>
      form{
         transform: scale(2);
         transform-origin: top left;
      }
    </style>
       <form action="/detect" method="post" enctype="multipart/form-data">
          <input type="file" name="file"></br>
          <input type="submit" value="전송">
       </form>
        
    '''
@app.route('/detect', methods=['GET','POST']) # root 경로에서 넘어 온 이미지 받는 페이지
def detect():
    # request 관련 페이지들은
    # route 설정 시 반드시 전송방식을 정의해야 한다

    # GET  -> request.args['Key값']
    # POST -> request.form['Key값']
    # file -> request.files['Key값']


  
    
    #받아오는 코드
    f=request.files['file']
    filename=secure_filename(f.filename)
    img_path='static/imgs/'+ filename
    f.save(img_path)

    i = ImageDetect() #대문자로 시작, ()가 있으니 클래스임을 알 수 있음
    result=i.detect_img(img_path)

    if result.size == 0:
        return '<h2>탐색 결과 없음</h2>'
    
    cnf=result[0][4] #신뢰도
    nc=int(result[0][5])
    label=i.data[nc]
    output='<h2>{}일 확률이 {:.2f}%입니다</h2>'.format(label,cnf*100)
    
    return output
                    
    # file 관련 경로, 이름들은 보안을 지켜주자

# 내가 직접 실행(run)시 내장 변수name이 ___main__으로 변함
if __name__ == '__main__':
    app.run(port=5021) 

