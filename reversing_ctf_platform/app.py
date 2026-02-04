from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, validators
from wtforms.validators import DataRequired, Length, ValidationError
import bcrypt
import os
import zipfile
from datetime import datetime
import secrets
import atexit
import glob

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ctf_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = True

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    submissions = db.relationship('Submission', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """안전한 비밀번호 해싱"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """비밀번호 검증"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def get_solved_problems(self):
        """해결한 문제 목록 반환"""
        return [sub.problem_id for sub in self.submissions if sub.is_correct]
    
    def __repr__(self):
        return f'<User {self.username}>'

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(20), nullable=False)  # easy, medium, hard
    points = db.Column(db.Integer, nullable=False)
    flag = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    submissions = db.relationship('Submission', backref='problem', lazy=True)
    
    def __repr__(self):
        return f'<Problem {self.problem_id}>'

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    problem_id = db.Column(db.String(50), db.ForeignKey('problem.problem_id'), nullable=False)
    submitted_flag = db.Column(db.String(200), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    points_earned = db.Column(db.Integer, default=0)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))  # IPv6 지원
    
    # Unique constraint: 한 사용자는 한 문제당 하나의 정답만
    __table_args__ = (db.UniqueConstraint('user_id', 'problem_id', 'is_correct', name='unique_correct_submission'),)
    
    def __repr__(self):
        return f'<Submission {self.user_id}-{self.problem_id}>'

# WTForms for CSRF protection and validation
class LoginForm(FlaskForm):
    username = StringField('사용자명', [
        DataRequired(message='사용자명을 입력하세요.'),
        Length(min=3, max=80, message='사용자명은 3-80자 사이여야 합니다.')
    ])
    password = PasswordField('비밀번호', [
        DataRequired(message='비밀번호를 입력하세요.'),
        Length(min=4, message='비밀번호는 최소 4자 이상이어야 합니다.')
    ])

class RegisterForm(FlaskForm):
    username = StringField('사용자명', [
        DataRequired(message='사용자명을 입력하세요.'),
        Length(min=3, max=80, message='사용자명은 3-80자 사이여야 합니다.')
    ])
    password = PasswordField('비밀번호', [
        DataRequired(message='비밀번호를 입력하세요.'),
        Length(min=6, message='비밀번호는 최소 6자 이상이어야 합니다.')
    ])
    
    def validate_username(self, field):
        """사용자명 중복 검사"""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('이미 사용 중인 사용자명입니다.')

class FlagSubmissionForm(FlaskForm):
    problem_id = StringField('문제 ID', [DataRequired()])
    flag = StringField('플래그', [
        DataRequired(message='플래그를 입력하세요.'),
        Length(min=5, max=200, message='플래그 길이가 올바르지 않습니다.')
    ])

def init_problems():
    """초기 문제 데이터 생성"""
    problems_data = [
        # Easy Problems
        {"problem_id": "easy_01", "title": "Simple String", "category": "easy", "points": 50, "flag": "FLAG{simple_string_comparison}", "description": "간단한 문자열 비교 문제입니다."},
        {"problem_id": "easy_02", "title": "Magic Number", "category": "easy", "points": 50, "flag": "FLAG{the_answer_to_everything}", "description": "특별한 숫자를 찾아보세요."},
        {"problem_id": "easy_03", "title": "Math Problem", "category": "easy", "points": 50, "flag": "FLAG{math_is_easy}", "description": "간단한 수학 문제입니다."},
        {"problem_id": "easy_04", "title": "String Length", "category": "easy", "points": 50, "flag": "FLAG{reverse_engineering}", "description": "문자열의 길이와 특정 문자를 확인합니다."},
        {"problem_id": "easy_05", "title": "Multiplication", "category": "easy", "points": 50, "flag": "FLAG{multiplication_master}", "description": "곱셈 연산을 수행합니다."},
        {"problem_id": "easy_06", "title": "Character Check", "category": "easy", "points": 50, "flag": "FLAG{uppercase_letter}", "description": "문자의 종류를 확인합니다."},
        {"problem_id": "easy_07", "title": "Array Search", "category": "easy", "points": 50, "flag": "FLAG{array_search_success}", "description": "배열에서 값을 찾습니다."},
        {"problem_id": "easy_08", "title": "Even Number", "category": "easy", "points": 50, "flag": "FLAG{even_positive_number}", "description": "짝수인지 확인합니다."},
        {"problem_id": "easy_09", "title": "Admin Access", "category": "easy", "points": 50, "flag": "FLAG{admin_access_granted}", "description": "관리자 권한을 얻어보세요."},
        {"problem_id": "easy_10", "title": "Lucky Number", "category": "easy", "points": 50, "flag": "FLAG{lucky_number_seven}", "description": "행운의 숫자를 맞춰보세요."},
        
        # Medium Problems
        {"problem_id": "medium_01", "title": "Caesar Cipher", "category": "medium", "points": 100, "flag": "FLAG{caesar_cipher_decoded}", "description": "시저 암호를 해독하세요."},
        {"problem_id": "medium_02", "title": "Fibonacci", "category": "medium", "points": 100, "flag": "FLAG{fibonacci_sequence_master}", "description": "피보나치 수열 문제입니다."},
        {"problem_id": "medium_03", "title": "Checksum", "category": "medium", "points": 100, "flag": "FLAG{checksum_validation_passed}", "description": "체크섬을 계산하세요."},
        {"problem_id": "medium_04", "title": "Transform", "category": "medium", "points": 100, "flag": "FLAG{mathematical_transformation}", "description": "수학적 변환을 분석하세요."},
        {"problem_id": "medium_05", "title": "XOR Cipher", "category": "medium", "points": 100, "flag": "FLAG{xor_encryption_cracked}", "description": "XOR 암호화를 해독하세요."},
        {"problem_id": "medium_06", "title": "Prime Number", "category": "medium", "points": 100, "flag": "FLAG{prime_number_in_range}", "description": "소수를 찾아보세요."},
        {"problem_id": "medium_07", "title": "String Reverse", "category": "medium", "points": 100, "flag": "FLAG{string_reversal_success}", "description": "문자열을 뒤집어보세요."},
        {"problem_id": "medium_08", "title": "Bitwise Ops", "category": "medium", "points": 100, "flag": "FLAG{bitwise_operations_master}", "description": "비트 연산을 분석하세요."},
        {"problem_id": "medium_09", "title": "License Key", "category": "medium", "points": 100, "flag": "FLAG{license_validation_bypassed}", "description": "라이센스 키를 우회하세요."},
        {"problem_id": "medium_10", "title": "Factorial", "category": "medium", "points": 100, "flag": "FLAG{factorial_function_identified}", "description": "팩토리얼 함수를 식별하세요."},
        
        # Hard Problems
        {"problem_id": "hard_01", "title": "DJB2 Hash", "category": "hard", "points": 200, "flag": "FLAG{djb2_hash_algorithm}", "description": "DJB2 해시 알고리즘을 분석하세요."},
        {"problem_id": "hard_02", "title": "Obfuscated String", "category": "hard", "points": 200, "flag": "FLAG{obfuscated_string_manipulation}", "description": "난독화된 문자열을 해독하세요."},
        {"problem_id": "hard_03", "title": "Anti Debug", "category": "hard", "points": 200, "flag": "FLAG{anti_debug_bypassed}", "description": "안티 디버깅을 우회하세요."},
        {"problem_id": "hard_04", "title": "CRC32", "category": "hard", "points": 200, "flag": "FLAG{crc32_checksum_cracked}", "description": "CRC32 체크섬을 크랙하세요."},
        {"problem_id": "hard_05", "title": "Multi XOR", "category": "hard", "points": 200, "flag": "FLAG{multi_key_xor_decrypted}", "description": "다중 키 XOR을 해독하세요."},
        {"problem_id": "hard_06", "title": "Serial Validation", "category": "hard", "points": 200, "flag": "FLAG{complex_serial_validation}", "description": "복잡한 시리얼 검증을 우회하세요."},
        {"problem_id": "hard_07", "title": "Virtual Machine", "category": "hard", "points": 200, "flag": "FLAG{virtual_machine_cracked}", "description": "가상머신을 분석하세요."},
        {"problem_id": "hard_08", "title": "Polymorphic", "category": "hard", "points": 200, "flag": "FLAG{polymorphic_time_based_check}", "description": "다형성 암호화를 해독하세요."},
        {"problem_id": "hard_09", "title": "Linked List", "category": "hard", "points": 200, "flag": "FLAG{linked_list_traversal}", "description": "링크드 리스트를 분석하세요."},
        {"problem_id": "hard_10", "title": "Self Modifying", "category": "hard", "points": 200, "flag": "FLAG{self_modifying_recursive_hash}", "description": "자기수정 코드를 분석하세요."}
    ]
    
    for problem_data in problems_data:
        existing = Problem.query.filter_by(problem_id=problem_data['problem_id']).first()
        if not existing:
            problem = Problem(**problem_data)
            db.session.add(problem)
    
    db.session.commit()

def cleanup_temp_files():
    """임시 ZIP 파일들 정리"""
    try:
        zip_files = glob.glob(os.path.join(os.path.dirname(__file__), '*_problems.zip'))
        for zip_file in zip_files:
            if os.path.exists(zip_file):
                os.remove(zip_file)
                app.logger.info(f'Cleaned up temporary file: {zip_file}')
    except Exception as e:
        app.logger.error(f'Error cleaning up temp files: {e}')

def find_executable_file(category, problem_num):
    """실행 파일을 여러 경로에서 찾기"""
    base_dir = os.path.dirname(__file__)
    
    possible_paths = [
        # 현재 폴더 내
        os.path.join(base_dir, 'compiled_executables', category, f'problem_{problem_num}.exe'),
        # 상위 폴더의 reversing_challenges
        os.path.join(base_dir, '..', 'reversing_challenges', 'compiled_executables', category, f'problem_{problem_num}.exe'),
        # 같은 레벨의 reversing_challenges
        os.path.join(base_dir, 'reversing_challenges', 'compiled_executables', category, f'problem_{problem_num}.exe'),
        # 절대 경로로 찾기
        os.path.join(os.path.dirname(base_dir), 'reversing_challenges', 'compiled_executables', category, f'problem_{problem_num}.exe'),
        # 현재 작업 디렉토리 기준
        os.path.join(os.getcwd(), 'reversing_challenges', 'compiled_executables', category, f'problem_{problem_num}.exe'),
        # 상대 경로 (다양한 시도)
        f'../reversing_challenges/compiled_executables/{category}/problem_{problem_num}.exe',
        f'reversing_challenges/compiled_executables/{category}/problem_{problem_num}.exe',
        f'compiled_executables/{category}/problem_{problem_num}.exe'
    ]
    
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            app.logger.info(f'Found executable: {abs_path}')
            return abs_path
    
    app.logger.error(f'Executable not found for {category}/problem_{problem_num}.exe. Tried paths: {possible_paths}')
    return None

def create_tables():
    """데이터베이스 테이블 생성 및 초기 데이터 설정"""
    with app.app_context():
        db.create_all()
        init_problems()
    """데이터베이스 테이블 생성 및 초기 데이터 설정"""
    with app.app_context():
        db.create_all()
        init_problems()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or not user.is_active:
        session.clear()
        return redirect(url_for('login'))
    
    # 카테고리별 문제 조회
    easy_problems = Problem.query.filter_by(category='easy', is_active=True).all()
    medium_problems = Problem.query.filter_by(category='medium', is_active=True).all()
    hard_problems = Problem.query.filter_by(category='hard', is_active=True).all()
    
    # 사용자가 해결한 문제 목록
    solved_problems = user.get_solved_problems()
    
    problems = {
        'easy': easy_problems,
        'medium': medium_problems,
        'hard': hard_problems
    }
    
    return render_template('index.html', problems=problems, solved_problems=solved_problems, user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data
        
        # SQL 인젝션 방지
        user = User.query.filter_by(username=username, is_active=True).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            
            # 마지막 로그인 시간 업데이트
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            flash(f'환영합니다, {user.username}님!', 'success')
            return redirect(url_for('index'))
        else:
            flash('잘못된 사용자명 또는 비밀번호입니다.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data
        
        try:
            # 새 사용자 생성
            user = User(username=username)
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            # 자동 로그인
            session['user_id'] = user.id
            session['username'] = user.username
            
            flash(f'회원가입이 완료되었습니다. 환영합니다, {user.username}님!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            db.session.rollback()
            flash('회원가입 중 오류가 발생했습니다. 다시 시도해주세요.', 'error')
    
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    username = session.get('username', '익명')
    session.clear()
    flash(f'{username}님, 안전하게 로그아웃되었습니다.', 'info')
    return redirect(url_for('login'))

@app.route('/submit', methods=['POST'])
def submit_flag():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '로그인이 필요합니다.'})
    
    form = FlagSubmissionForm()
    
    if not form.validate_on_submit():
        return jsonify({'success': False, 'message': '잘못된 요청입니다.'})
    
    user_id = session['user_id']
    problem_id = form.problem_id.data.strip()
    submitted_flag = form.flag.data.strip()
    
    try:
        # 사용자 및 문제 조회 
        user = User.query.get(user_id)
        problem = Problem.query.filter_by(problem_id=problem_id, is_active=True).first()
        
        if not user or not user.is_active:
            return jsonify({'success': False, 'message': '유효하지 않은 사용자입니다.'})
        
        if not problem:
            return jsonify({'success': False, 'message': '존재하지 않는 문제입니다.'})
        
        # 이미 해결한 문제인지 확인
        existing_correct = Submission.query.filter_by(
            user_id=user_id, 
            problem_id=problem_id, 
            is_correct=True
        ).first()
        
        if existing_correct:
            return jsonify({'success': False, 'message': '이미 해결한 문제입니다.'})
        
        # 플래그 검증
        is_correct = (submitted_flag == problem.flag)
        points_earned = problem.points if is_correct else 0
        
        # 제출 기록 저장
        submission = Submission(
            user_id=user_id,
            problem_id=problem_id,
            submitted_flag=submitted_flag,
            is_correct=is_correct,
            points_earned=points_earned,
            ip_address=request.remote_addr
        )
        
        db.session.add(submission)
        
        # 정답인 경우 사용자 점수 업데이트
        if is_correct:
            user.score += points_earned
        
        db.session.commit()
        
        if is_correct:
            return jsonify({
                'success': True, 
                'message': f'정답입니다! +{points_earned}점 획득!',
                'points': points_earned
            })
        else:
            return jsonify({'success': False, 'message': '틀렸습니다. 다시 시도해보세요.'})
            
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Flag submission error: {e}')
        return jsonify({'success': False, 'message': '서버 오류가 발생했습니다.'})

@app.route('/scoreboard')
def scoreboard():
    # 점수 순으로 사용자 조회 
    users = User.query.filter_by(is_active=True).order_by(User.score.desc(), User.created_at.asc()).all()
    
    scoreboard_data = []
    for user in users:
        solved_count = Submission.query.filter_by(user_id=user.id, is_correct=True).count()
        scoreboard_data.append({
            'username': user.username,
            'score': user.score,
            'solved_count': solved_count,
            'join_date': user.created_at.strftime('%Y-%m-%d'),
            'last_login': user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'Never'
        })
    
    return render_template('scoreboard.html', scoreboard=scoreboard_data)

@app.route('/download/<problem_id>')
def download_problem(problem_id):
    """문제 파일 다운로드 - 미리 컴파일된 .exe 파일 사용"""
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'error')
        return redirect(url_for('login'))
    
    # 문제 존재 확인
    problem = Problem.query.filter_by(problem_id=problem_id, is_active=True).first()
    if not problem:
        flash('존재하지 않는 문제입니다.', 'error')
        return redirect(url_for('index'))
    
    # problem_id에서 카테고리와 문제 번호 추출
    # 예: easy_01 -> category=easy, problem_num=01
    parts = problem_id.split('_')
    if len(parts) != 2:
        flash('잘못된 문제 ID입니다.', 'error')
        return redirect(url_for('index'))
    
    category = parts[0]  # easy, medium, hard
    problem_num = parts[1]  # 01, 02, ..., 10
    
    # 실행 파일 찾기
    exe_file_path = find_executable_file(category, problem_num)
    
    if not exe_file_path:
        flash(f'문제 파일을 찾을 수 없습니다. ({problem_id})', 'error')
        return redirect(url_for('index'))
    
    try:
        # .exe 파일 다운로드
        return send_file(exe_file_path, as_attachment=True, 
                        download_name=f'{problem_id}.exe')
        
    except Exception as e:
        app.logger.error(f'Download error for {problem_id}: {e}')
        flash('파일 다운로드 중 오류가 발생했습니다.', 'error')
        return redirect(url_for('index'))

@app.route('/download_all/<category>')
def download_all_problems(category):
    """카테고리별 모든 문제 다운로드 (ZIP) - 미리 컴파일된 .exe 파일 사용"""
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'error')
        return redirect(url_for('login'))
    
    if category not in ['easy', 'medium', 'hard']:
        flash('잘못된 카테고리입니다.', 'error')
        return redirect(url_for('index'))
    
    try:
        # 임시 ZIP 파일 생성 (현재 디렉토리에)
        zip_filename = f'{category}_problems.zip'
        zip_path = os.path.join(os.path.dirname(__file__), zip_filename)
        
        # 기존 ZIP 파일이 있으면 삭제
        if os.path.exists(zip_path):
            os.remove(zip_path)
        
        files_added = 0
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            # 해당 카테고리의 모든 문제 추가
            problems = Problem.query.filter_by(category=category, is_active=True).all()
            
            for problem in problems:
                # problem_id에서 문제 번호 추출 (예: easy_01 -> 01)
                parts = problem.problem_id.split('_')
                if len(parts) == 2:
                    problem_num = parts[1]  # 01, 02, ..., 10
                    
                    # 실행 파일 찾기
                    exe_path = find_executable_file(category, problem_num)
                    
                    if exe_path:
                        # .exe 파일을 ZIP에 추가
                        zipf.write(exe_path, f'{problem.problem_id}.exe')
                        files_added += 1
                        app.logger.info(f'Added {problem.problem_id}.exe to ZIP from {exe_path}')
                    else:
                        app.logger.warning(f'File not found for {problem.problem_id}')
        
        if files_added == 0:
            flash(f'{category} 카테고리의 문제 파일을 찾을 수 없습니다.', 'error')
            if os.path.exists(zip_path):
                os.remove(zip_path)
            return redirect(url_for('index'))
        
        app.logger.info(f'Created ZIP with {files_added} files: {zip_path}')
        
        # 다운로드 후 파일 정리를 위한 콜백 함수 등록
        def cleanup_after_send():
            try:
                if os.path.exists(zip_path):
                    os.remove(zip_path)
                    app.logger.info(f'Cleaned up ZIP file: {zip_path}')
            except Exception as e:
                app.logger.error(f'Error cleaning up ZIP file {zip_path}: {e}')
        
        # 응답 후 정리 작업 예약
        import threading
        timer = threading.Timer(30.0, cleanup_after_send)  # 30초 후 정리
        timer.start()
        
        return send_file(zip_path, as_attachment=True, 
                        download_name=f'{category}_reversing_problems.zip')
        
    except Exception as e:
        app.logger.error(f'Bulk download error for {category}: {e}')
        flash('파일 다운로드 중 오류가 발생했습니다.', 'error')
        return redirect(url_for('index'))
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('login'))
    
    # 사용자의 제출 기록
    submissions = Submission.query.filter_by(user_id=user.id, is_correct=True).order_by(Submission.submitted_at.desc()).all()
    
    return render_template('profile.html', user=user, submissions=submissions)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404, error_message='페이지를 찾을 수 없습니다.'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', error_code=500, error_message='서버 내부 오류가 발생했습니다.'), 500

if __name__ == '__main__':
    # 앱 종료 시 임시 파일 정리
    atexit.register(cleanup_temp_files)
    
    # 데이터베이스 초기화
    create_tables()
    
    app.run(debug=True, host='0.0.0.0', port=5000)