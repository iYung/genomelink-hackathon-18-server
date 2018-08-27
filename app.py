from flask import Flask, flash, render_template, request, redirect, session, url_for
import genomelink
import json

def create_app():
    app = Flask(__name__)


    @app.route('/')
    def index():
        authorize_url = genomelink.OAuth.authorize_url(scope=['report:intelligence report:depression report:openness report:extraversion'])

        # Fetching a protected resource using an OAuth2 token if exists.
        reports = []
        userToken = ""
        jsonReports = []
        if session.get('oauth_token'):
            for name in ["intelligence", "depression", "openness", "extraversion"]:
                reports.append(genomelink.Report.fetch(name=name, population='european', token=session['oauth_token']))
            userToken = session['oauth_token']['access_token']
            for report in reports:
                jsonReports.append(report.summary["score"])
        return render_template('index.html', authorize_url=authorize_url, reports=jsonReports, token=userToken)

    @app.route('/callback')
    def callback():
        # The user has been redirected back from the provider to your registered
        # callback URL. With this redirection comes an authorization code included
        # in the request URL. We will use that to obtain an access token.
        try:
            token = genomelink.OAuth.token(request_url=request.url)
        except genomelink.errors.GenomeLinkError as e:
            flash('Authorization failed.')
            if os.environ.get('DEBUG') == '1':
                flash('[DEBUG] ({}) {}'.format(e.error, e.description))
            return redirect(url_for('index'))

        # At this point you can fetch protected resources but lets save
        # the token and show how this is done from a persisted token in index page.
        session['oauth_token'] = token
        return redirect(url_for('index'))

    return app

if __name__ == '__main__':
    # This allows us to use a plain HTTP callback.
    import os
    os.environ['DEBUG'] = '1'
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Run local server on port 5000.
    app = create_app()
    app.secret_key = os.urandom(24)
    print os.environ['PORT']
    app.run(debug=True, host='0.0.0.0', port=os.environ['PORT'])
