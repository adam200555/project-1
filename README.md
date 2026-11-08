# Project 1 - Neo4j school graph (Git + Docker Compose + Linux)

A Python script that stores students, courses and teachers in Neo4j,
running in Docker Compose with a persistent volume.

## Run it

```bash
docker compose up -d          # start Neo4j (data kept in a volume)
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Neo4j Browser: http://localhost:7474 (user `neo4j`, password `password123`)

```bash
docker compose stop           # stop, keep data
docker compose down           # remove container, keep data (volume)
docker compose down -v        # remove container AND data (careful!)
```

## 4-week plan

### Week 1 - Linux (use WSL on Windows: `wsl --install`)
- [ ] Navigate: `pwd ls cd mkdir touch cp mv rm`
- [ ] Read files: `cat less head tail grep`
- [ ] Permissions: `chmod chown ls -l`
- [ ] Processes/network: `ps top kill curl ping ss`
- [ ] Write one bash script (e.g. `backup.sh` that dumps the Neo4j volume)

### Week 2 - Git & GitHub
- [ ] `git init`, `git add`, `git commit`, `git log`
- [ ] Branches: `git switch -c feature/x`, `git merge`
- [ ] Push to GitHub, open a pull request on your own repo
- [ ] Write good commit messages ("Add seed script", not "update")

```bash
git init
git add .
git commit -m "Initial commit: Neo4j compose + seed script"
git branch -M main
git remote add origin https://github.com/<you>/project-1.git
git push -u origin main
```

### Week 3 - Docker Compose
- [ ] Understand services, ports, volumes, environment
- [ ] Add a second service: a Flask API container that talks to Neo4j
- [ ] Move the password to a `.env` file
- [ ] Use `docker compose logs -f`, `exec`, `ps`

### Week 4 - Pick a direction and extend
- Web: Flask/Django API + simple front end on top of the graph
- Security: scan your own stack, write a short report
- Data: recommendation queries (friends of friends, same courses)

## Done when
- [ ] `docker compose up -d && python app.py` works on a clean machine
- [ ] Repo is public with this README
- [ ] At least 10 meaningful commits and 1 pull request
