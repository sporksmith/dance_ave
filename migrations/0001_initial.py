# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SongStation'
        db.create_table(u'dance_ave_songstation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('audio_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('select_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('complete_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'dance_ave', ['SongStation'])

        # Adding model 'Player'
        db.create_table(u'dance_ave_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
        ))
        db.send_create_signal(u'dance_ave', ['Player'])

        # Adding M2M table for field completed_stations on 'Player'
        db.create_table(u'dance_ave_player_completed_stations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('player', models.ForeignKey(orm[u'dance_ave.player'], null=False)),
            ('songstation', models.ForeignKey(orm[u'dance_ave.songstation'], null=False))
        ))
        db.create_unique(u'dance_ave_player_completed_stations', ['player_id', 'songstation_id'])


    def backwards(self, orm):
        # Deleting model 'SongStation'
        db.delete_table(u'dance_ave_songstation')

        # Deleting model 'Player'
        db.delete_table(u'dance_ave_player')

        # Removing M2M table for field completed_stations on 'Player'
        db.delete_table('dance_ave_player_completed_stations')


    models = {
        u'dance_ave.player': {
            'Meta': {'object_name': 'Player'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'completed_stations': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dance_ave.SongStation']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'dance_ave.songstation': {
            'Meta': {'object_name': 'SongStation'},
            'audio_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'complete_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'select_code': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['dance_ave']