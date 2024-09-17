# Generated by Django 3.2.13 on 2024-09-12 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authors', models.CharField(max_length=50, verbose_name='Автор')),
                ('name', models.CharField(max_length=200, verbose_name='Название книги')),
                ('publication_number', models.IntegerField(default=0, verbose_name='Номер')),
                ('page_number', models.IntegerField(default=0, verbose_name='Количество страниц')),
                ('publication_date', models.DateField(null=True, verbose_name='Дата издания')),
                ('description', models.CharField(max_length=1000, verbose_name='Описание')),
                ('isbn', models.CharField(max_length=100, null=True, verbose_name='ISBN')),
            ],
            options={
                'db_table': 'book_card',
            },
        ),
        migrations.CreateModel(
            name='BookRack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField(default=0, verbose_name='Номер стеллажа')),
            ],
            options={
                'db_table': 'book_rack',
            },
        ),
        migrations.CreateModel(
            name='BookShelf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField(default=0, verbose_name='Номер полки')),
                ('rack', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shelfs', to='admin.bookrack')),
            ],
            options={
                'db_table': 'book_shelf',
                'unique_together': {('name', 'rack')},
            },
        ),
        migrations.CreateModel(
            name='Librarian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=30, verbose_name='Имя')),
                ('fired', models.BooleanField(default=False, verbose_name='Уволен')),
            ],
            options={
                'db_table': 'librarian',
            },
        ),
        migrations.CreateModel(
            name='PublicationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Вид издания')),
            ],
            options={
                'db_table': 'publication_type',
            },
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=30, verbose_name='Имя')),
            ],
            options={
                'db_table': 'reader',
            },
        ),
        migrations.CreateModel(
            name='ReaderCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt_date', models.DateField(verbose_name='Дата получения')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='admin.reader')),
            ],
            options={
                'db_table': 'reader_card',
            },
        ),
        migrations.CreateModel(
            name='MovementJournal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('move_date', models.DateField(verbose_name='Дата перемещения')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='m_journal', to='admin.bookcard')),
                ('book_shelf_new', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='new_shelfs', to='admin.bookshelf')),
                ('book_shelf_old', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='old_shelfs', to='admin.bookshelf')),
            ],
            options={
                'db_table': 'movement_journal',
            },
        ),
        migrations.CreateModel(
            name='BookRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField(default=0, verbose_name='Номер зала')),
                ('librarian', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='admin.librarian')),
            ],
            options={
                'db_table': 'book_room',
            },
        ),
        migrations.AddField(
            model_name='bookrack',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='racks', to='admin.bookroom'),
        ),
        migrations.CreateModel(
            name='BookIssueJournal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt_date', models.DateField(verbose_name='Дата выдачи')),
                ('outside_library', models.BooleanField(default=False, verbose_name='Чтение вне библиотеки')),
                ('returned', models.BooleanField(default=False, verbose_name='Возвращено')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='issue_journal', to='admin.bookcard')),
                ('reader_card', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='issue_journal', to='admin.readercard')),
            ],
            options={
                'db_table': 'book_issue_journal',
            },
        ),
        migrations.AddField(
            model_name='bookcard',
            name='book_shelf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='books', to='admin.bookshelf'),
        ),
        migrations.AddField(
            model_name='bookcard',
            name='publication_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='books', to='admin.publicationtype'),
        ),
        migrations.AlterUniqueTogether(
            name='bookrack',
            unique_together={('name', 'room')},
        ),
    ]