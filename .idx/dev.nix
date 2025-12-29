{ pkgs, ... }: {
  channel = "stable-23.11";

  packages = [
    # Node.js para frontend
    pkgs.nodejs_20
    pkgs.nodePackages.npm

    # Python para backend
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.virtualenv

    # Herramientas útiles
    pkgs.git
    pkgs.curl
    pkgs.jq
  ];

  env = {
    # Variables de entorno globales
    PYTHON_VERSION = "3.11";
    NODE_ENV = "development";
  };

  idx = {
    # Extensiones de VS Code
    extensions = [
      "ms-python.python"
      "ms-python.vscode-pylance"
      "bradlc.vscode-tailwindcss"
      "esbenp.prettier-vscode"
      "dbaeumer.vscode-eslint"
      "formulahendry.auto-rename-tag"
    ];

    workspace = {
      # Se ejecuta UNA vez al crear el workspace
      onCreate = {
        setup-frontend = ''
          cd frontend
          npm install
          echo "✅ Frontend dependencies installed"
        '';

        setup-backend = ''
          cd backend
          python -m venv venv
          source venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
          echo "✅ Backend dependencies installed"
        '';

        create-env-files = ''
          # Frontend .env.local
          echo 'NEXT_PUBLIC_API_URL=http://localhost:8000' > frontend/.env.local

          # Backend .env
          cat > backend/.env << 'EOF'
DATABASE_URL=sqlite:///./consolidador.db
SFTP_HOST=mft.positiva.gov.co
SFTP_PORT=2243
SFTP_USER=G_medica
SFTP_PASSWORD=your_password_here
SECRET_KEY=your-secret-key-change-in-production
DEBUG=true
EOF
          echo "✅ Environment files created"
        '';

        init-database = ''
          cd backend
          source venv/bin/activate
          python -c "from models.database import Base, engine; Base.metadata.create_all(bind=engine)"
          echo "✅ Database initialized"
        '';
      };

      # Se ejecuta cada vez que se abre el workspace
      onStart = {
        # Mensaje de bienvenida
        welcome = ''
          echo "🚀 Consolidador T25 - Firebase Studio"
          echo "=================================="
          echo "📂 Frontend: cd frontend && npm run dev"
          echo "🐍 Backend:  cd backend && source venv/bin/activate && uvicorn main:app --reload"
          echo ""
        '';
      };
    };

    # Previews automáticos
    previews = {
      enable = true;
      previews = {
        web = {
          command = ["npm" "run" "dev" "--" "--port" "$PORT" "--hostname" "0.0.0.0"];
          cwd = "frontend";
          manager = "web";
        };
      };
    };
  };
}
