from flask import Flask, render_template, request, redirect, url_for, session
from database import get_all_tables_data, delete_selected_rows

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session handling

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    # Dummy login, replace with actual check
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
    return '''
        <form method="post">
            <input type="text" name="username" placeholder="Admin Username">
            <input type="password" name="password" placeholder="Password">
            <button type="submit">Login</button>
        </form>
    '''

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        for table, rows in request.form.lists():
            if table != 'action' and request.form.get('action') == 'delete':
                delete_selected_rows(table, rows)

    tables_data = get_all_tables_data()
    return render_template('admin_dashboard.html', tables=tables_data)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
