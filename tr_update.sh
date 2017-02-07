#!/bin/sh

pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
pybabel update --previous -l zh -i messages.pot -o app/translations/zh/LC_MESSAGES/messages.po
vim app/translations/zh/LC_MESSAGES/messages.po
pybabel compile -d app/translations/

#msgmerge --update app/translations/zh/LC_MESSAGES/messages.po messages.pot
#vim app/translations/zh/LC_MESSAGES/messages.po
#msgfmt --output-file=app/translations/zh/LC_MESSAGES/messages.mo app/translations/zh/LC_MESSAGES/messages.po
