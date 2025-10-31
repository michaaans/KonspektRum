from flask import Blueprint, render_template, redirect, request, url_for, flash, abort
from flask_login import login_required, current_user

from ..extensions import db
from ..models.note import Note
from ..forms import CreateNoteForm, UpdateNoteForm

note = Blueprint('note', __name__)


@note.route('/note/create', methods=['GET', 'POST'])
@login_required
def create_note():
    form = CreateNoteForm()

    if form.validate_on_submit():

        note = Note(title=form.title.data,
                    content=form.content.data,
                    subject=form.subject.data,
                    teacher=form.teacher.data,
                    users_id=current_user.id)
        try:

            db.session.add(note)
            db.session.commit()
            flash('Конспект успешно создан!', 'success')
            return redirect(url_for('main.index'))

        except Exception as e:
            flash('Ошибка при создании конспекта', 'danger')
            print(f"Error creating note: {e}")

    return render_template('note/create.html', form=form)


@note.route('/note/<int:id>', methods=['GET'])
@login_required
def note_id(id):

    note = Note.query.get_or_404(id)

    return render_template('note/detail.html', note=note)


@note.route('/note/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_note(id):

    form = UpdateNoteForm()

    note = Note.query.get(id)

    # редактировать может только админ или учитель
    if note.author.id != current_user.id and not current_user.is_admin and not current_user.is_teacher:
        abort(403)

    if request.method == 'POST':

        note.title = form.title.data
        note.content = form.content.data
        note.subject = form.subject.data
        note.teacher = form.teacher.data

        try:
            db.session.commit()
            flash('Конспект успешно обновлен', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            flash('Упс.. Произошла ошибка', 'danger')
            print(str(e))

    return render_template('note/update.html', note=note, form=form)


@note.route('/note/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_note(id):

    note = Note.query.get(id)

    # удалять может только админ
    if note.author.id != current_user.id and not current_user.is_admin:
        abort(403)

    try:
        db.session.delete(note)
        db.session.commit()

        flash('Конспект успешно удален', 'success')
        return redirect(url_for('main.index'))

    except Exception as e:
        flash('Упс.. Произошла ошибка', 'danger')
        print(str(e))
