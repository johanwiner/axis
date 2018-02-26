#!/usr/bin/perl

package modern_self_defense_settings;
require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw($msd_name
	     $msd_day
             $msd_day2
             $msd_time
	     $msd_time2
	     $msd_place 
	     $list_size
	     $min_participants
	     $max_participants
	     $msd_instuctor 
	     $msd_instuctor_name
	     $mail_notification
	     $mail_min_participants_achieved
	     $min_participants_achieved_message
	     $mail_reminder
	     $mail_address
	     $message_required
	     $show_statistics
	     $show_user_pic
	     $show_participants_pic
	     $manual_dates
	     @msd_dates
	     @msd_times
	     $no_msd_message
	     @no_msd_dates);

use strict;
use utf8; 

use vars qw($msd_name);
use vars qw($msd_day);
use vars qw($msd_day2);
use vars qw($msd_time);
use vars qw($msd_time2);
use vars qw($msd_place);
use vars qw($list_size);
use vars qw($min_participants);
use vars qw($max_participants);
use vars qw($msd_instuctor);
use vars qw($msd_instuctor_name);
use vars qw($mail_notification);
use vars qw($mail_min_participants_achieved);
use vars qw($min_participants_achieved_message);
use vars qw($mail_reminder);
use vars qw($mail_address);
use vars qw($message_required);
use vars qw($show_statistics);
use vars qw($show_user_pic);
use vars qw($show_participants_pic);
use vars qw($manual_dates);
use vars qw(@msd_dates);
use vars qw(@msd_times);
use vars qw($no_msd_message);
use vars qw(@no_msd_dates);


# ---------- INSTÄLLNINGAR ---------- #

# Vad?
$msd_name           = "Modern Self Defense";

# Vilken dag?
$msd_day            = "Tisdag";
$msd_day2            = "Fredag";

# Vilken tid?
$msd_time           = "17:00-18:00";
$msd_time2           = "16:30-17:30";

# Var?
$msd_place          = "i Fitnessrummet i källaren i D-huset";

# Hur många pass kan man anmäla sig till åt gången?
$list_size            = 3;

# Minst antal deltagare per pass?
$min_participants          = 2;

# Max antal deltagare per pass?
$max_participants          = 16;

# Instruktören räknas in bland övriga deltagare? ja=1, nej=0
$msd_instuctor      = 1;

# Instruktörens mail alias?
$msd_instuctor_name = "johanwi";

# Skicka mail automatiskt om någon anmäler/avanmäler sig? ja=1, nej=0
$mail_notification    = 0;

# Skicka mail automatiskt när tillräckligt många är anmälda? ja=1, nej=0
$mail_min_participants_achieved = 1;

# Meddelande som ska skickas när tilräckligt många är anmälda?
$min_participants_achieved_message = "Det blir Modern Self Defense!";

# Skicka manuellt påminnelsemail? ja=1, nej=0
$mail_reminder        = 1;

# Mailadress att skicka till?
$mail_address         = "johanwi\@axis.com";

# Kräv meddelande av de som avanmäler sig? ja=1, nej=0
$message_required     = 0;

# Visa länk  till statistik sida? ja=1, nej=0
$show_statistics      = 1;

# Visa bild på inloggad användare? ja=1, nej=0
$show_user_pic        = 1;

# Visa bilder på alla anmälda? ja=1, nej=0
$show_participants_pic     = 1;

# Meddelande om det inte blir något pass?
$no_msd_message     = "Det blir ingen Modern Self Defense!";

# Ange datum när det blir pass manuellt? ja=1, nej=0
$manual_dates         = 0;

# Manuella datum och tidpunkt det blir pass
$msd_dates[0]       = "20160121";
$msd_times[0]       = "07:00-08:00";
$msd_dates[1]       = "20160127";
$msd_times[1]       = "07:00-08:00";
$msd_dates[2]       = "20160204";
$msd_times[2]       = "07:00-08:00";
$msd_dates[3]       = "20160210";
$msd_times[3]       = "07:00-08:00";
$msd_dates[4]       = "20160217";
$msd_times[4]       = "07:00-08:00";
$msd_dates[4]       = "20160224";
$msd_times[4]       = "07:00-08:00";


# Datum det inte blir något pass
$no_msd_dates[0]    = "20150527";
$no_msd_dates[1]    = "20150603";
$no_msd_dates[2]    = "20150617";

1;

