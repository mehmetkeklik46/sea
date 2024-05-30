from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
import sqlalchemy as sa
from app import db
from app.models import User


class LoginForm(FlaskForm):
    username = StringField(_l('Kullanıcı Adı'), validators=[DataRequired()])
    password = PasswordField(_l('Şifre'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Beni Hatırla'))
    submit = SubmitField(_l('Giriş Yap'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('Kullanıcı Adı'), validators=[DataRequired()])
    email = StringField(_l('E-posta'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Şifre'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Şifre Tekrarı'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Kayıt Ol'))

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError(_('Bu kullanıcı adı kullanılıyor. Lütfen farklı bir kullanıcı adı deneyin.'))

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError(_('Bu e-posta adresi kullanılıyor. Lütfen farklı bir e-posta adresi deneyin.'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('E-posta'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Şifre Sıfırlama'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Şifre'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Şifre Tekrarı'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Şifre Sıfırlama'))


class EditProfileForm(FlaskForm):
    username = StringField(_l('Kullanıcı Adı'), validators=[DataRequired()])
    about_me = TextAreaField(_l('Hakkımda'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Kaydet'))

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == self.username.data))
            if user is not None:
                raise ValidationError(_('Bu kullanıcı adı kullanılıyor. Lütfen farklı bir kullanıcı adı deneyin.'))


class EmptyForm(FlaskForm):
    submit = SubmitField('Kaydet')


class PostForm(FlaskForm):
    post = TextAreaField(_l('Bişeyler paylaş...'), validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Paylaş'))
