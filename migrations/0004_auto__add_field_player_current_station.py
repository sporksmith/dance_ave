# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Player.current_station'
        db.add_column(u'dance_ave_player', 'current_station',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='players_playing', null=True, to=orm['dance_ave.SongStation']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Player.current_station'
        db.delete_column(u'dance_ave_player', 'current_station_id')


    models = {
        u'dance_ave.player': {
            'Meta': {'object_name': 'Player'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'completed_stations': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dance_ave.SongStation']", 'symmetrical': 'False'}),
            'current_station': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players_playing'", 'null': 'True', 'to': u"orm['dance_ave.SongStation']"}),
            'finish_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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