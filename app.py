import os
from ChatApp import app

# Default port is 5000 unless $PORT if defined.
port = int(os.environ.get('PORT', 5000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=True)
