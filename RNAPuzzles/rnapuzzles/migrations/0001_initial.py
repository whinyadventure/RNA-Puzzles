# Generated by Django 2.2.7 on 2020-01-16 19:53

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import rnapuzzles.models.puzzles
import rnapuzzles.models.user


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last name')),
                ('institution', models.CharField(blank=True, max_length=150, verbose_name='institution')),
                ('role', models.PositiveSmallIntegerField(choices=[(1, 'Organizer'), (2, 'Participant'), (3, 'Group Leader')], default=0)),
                ('member_authorized', models.BooleanField(default=False)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('is_authorised', models.BooleanField(default=False)),
                ('is_disabled', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', rnapuzzles.models.user.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.IntegerField(default=1, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField(verbose_name='Opening date')),
                ('end_date', models.DateTimeField(verbose_name='Closing date')),
                ('end_automatic', models.DateTimeField(verbose_name='Closing automatic date')),
                ('result_published', models.BooleanField(default=False)),
                ('author', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-puzzle_info', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FaqModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ResourcesModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('SB', 'Submitted'), ('WA', 'Waiting'), ('EV', 'Evaluation'), ('IN', 'Error'), ('SU', ' Success')], default='SB', max_length=2)),
                ('challenge', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='rnapuzzles.Challenge')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PuzzleInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=250, verbose_name='Description')),
                ('sequence', models.TextField(verbose_name="RNA sequence (5' to 3')")),
                ('publish_date', models.DateTimeField(blank=True, null=True, verbose_name='Target 3D structure publication date')),
                ('reference', models.TextField(blank=True, verbose_name='Reference')),
                ('reference_url', models.URLField(blank=True, verbose_name='Reference URL')),
                ('pdb_id', models.CharField(blank=True, max_length=4, verbose_name='PDB ID')),
                ('pdb_url', models.URLField(blank=True, verbose_name='PDB URL')),
                ('pdb_file', models.FileField(blank=True, upload_to='', verbose_name='Target 3D structure file')),
                ('img', models.ImageField(blank=True, upload_to=rnapuzzles.models.puzzles.puzzle_info_img_filename, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])], verbose_name='Target 3D structure graphic representation')),
                ('author', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('metrics', models.ManyToManyField(to='rnapuzzles.Metric')),
            ],
            options={
                'verbose_name': 'Puzzle Information',
            },
        ),
        migrations.CreateModel(
            name='NewsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('publish_at', models.DateTimeField(null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['public', '-publish_at'],
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=30, unique=True, verbose_name='group name')),
                ('group_description', models.TextField(blank=True)),
                ('contact', models.EmailField(blank=True, max_length=254)),
                ('leader', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('name_group', 'Can change the name of the Group'), ('accept_group', 'Can accept user for group')],
            },
        ),
        migrations.CreateModel(
            name='ChallengeFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(blank=True, help_text='Information about file content. Maximum 50 characters.', max_length=50)),
                ('file', models.FileField(blank=True, upload_to='')),
                ('challenge', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='rnapuzzles.Challenge')),
            ],
        ),
        migrations.AddField(
            model_name='challenge',
            name='puzzle_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rnapuzzles.PuzzleInfo'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='group_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rnapuzzles.Group'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Error'), (1, 'Success')])),
                ('score', models.FloatField()),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rnapuzzles.Challenge')),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rnapuzzles.Metric')),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rnapuzzles.Submission')),
            ],
            options={
                'unique_together': {('submission', 'metric')},
            },
        ),
    ]
