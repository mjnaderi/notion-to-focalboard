A simple web app to convert Notion export to Focalboard (Mattermost Boards) archive.

[Related Focalboard Doc](https://docs.mattermost.com/boards/data-and-archives.html#import-from-notion)

## Usage

- Run the django project.
- Clone focalboard repository and install node dependencies.

  ```
  git clone -b v0.15.0 git@github.com:mattermost/focalboard.git
  cd webapp
  npm install
  cd ../import/notion
  npm install
  ```

  Note: Replace `v0.15.0` with your version of Focalboard.

- Run this manage.py command:

  ```
  python manage.py convert /PATH/TO/FOCALBOARD/REPO
  ```