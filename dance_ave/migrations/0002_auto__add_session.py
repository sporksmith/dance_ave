# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Session'
        db.create_table(u'dance_ave_session', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dance_ave.Player'])),
        ))
        db.send_create_signal(u'dance_ave', ['Session'])

        # Adding index on 'SongStation', fields ['complete_code']
        db.create_index(u'dance_ave_songstation', ['complete_code'])

        # Adding index on 'SongStation', fields ['select_code']
        db.create_index(u'dance_ave_songstation', ['select_code'])


    def backwards(self, orm):
        # Removing index on 'SongStation', fields ['select_code']
        db.delete_index(u'dance_ave_songstation', ['select_code'])

        # Removing index on 'SongStation', fields ['complete_code']
        db.delete_index(u'dance_ave_songstation', ['complete_code'])

        # Deleting model 'Session'
        db.delete_table(u'dance_ave_session')


    models = {
        u'dance_ave.player': {
            'Meta': {'object_name': 'Player'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'completed_stations': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dance_ave.SongStation']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'dance_ave.session': {
            'Meta': {'object_name': 'Session'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dance_ave.Player']"})
        },
        u'dance_ave.songstation': {
            'Meta': {'object_name': 'SongStation'},
            'audio_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'complete_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'select_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'})
        }
    }

    complete_apps = ['dance_ave']