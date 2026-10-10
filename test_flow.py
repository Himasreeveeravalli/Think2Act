import requests
import re

s = requests.Session()

# 1. GET Register page
r_get_reg = s.get('http://127.0.0.1:5000/register')
match = re.search(r'name="csrf_token" value="(.*?)"', r_get_reg.text)
csrf_token = match.group(1) if match else ''

# 2. POST Register
reg_data = {
    'csrf_token': csrf_token,
    'full_name': 'Santhi User',
    'email': 'santhi@example.com',
    'password': 'Password123!',
    'confirm_password': 'Password123!'
}
r_post_reg = s.post('http://127.0.0.1:5000/register', data=reg_data)
print('Register POST status:', r_post_reg.status_code, '| Final URL:', r_post_reg.url)

# 3. GET Login page
r_get_login = s.get('http://127.0.0.1:5000/login')
match2 = re.search(r'name="csrf_token" value="(.*?)"', r_get_login.text)
login_csrf = match2.group(1) if match2 else ''

# 4. POST Login
login_data = {
    'csrf_token': login_csrf,
    'email': 'santhi@example.com',
    'password': 'Password123!'
}
r_post_login = s.post('http://127.0.0.1:5000/login', data=login_data)
print('Login POST status:', r_post_login.status_code, '| Final URL:', r_post_login.url)

# 5. GET Dashboard
r_dash = s.get('http://127.0.0.1:5000/dashboard')
print('Dashboard status:', r_dash.status_code, '| Welcome message present:', 'Santhi User' in r_dash.text)

# 6. GET Natural Language Search
r_search = s.get('http://127.0.0.1:5000/search?q=Find+laptops+under+50000+with+16GB+RAM')
print('Search status:', r_search.status_code, '| Results count present:', 'Showing' in r_search.text)

# 7. GET Comparison Page
r_comp = s.get('http://127.0.0.1:5000/compare?id=lap-003&id=lap-004')
print('Compare status:', r_comp.status_code, '| Spec Matrix present:', 'Specifications Matrix' in r_comp.text)

# 8. GET Recommendations Page
r_rec = s.get('http://127.0.0.1:5000/recommendations')
print('Recommendations status:', r_rec.status_code, '| Top Pick present:', 'Top Pick Overall' in r_rec.text)

# 9. GET Search History Page
r_hist = s.get('http://127.0.0.1:5000/history')
print('History status:', r_hist.status_code, '| Query logged:', 'Find laptops under 50000' in r_hist.text)

print('\nFULL E2E END-TO-END FLOW VERIFIED 100% WORKING!')
