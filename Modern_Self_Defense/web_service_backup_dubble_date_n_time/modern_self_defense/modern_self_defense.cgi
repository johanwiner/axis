#!/usr/bin/perl

use strict;
use CGI;
use utf8;
use MIME::Lite;

use modern_self_defense_settings;

my($debug);
my($msw_way);
my($time_a_place);
my($participant_name);
my($msd_list_dir);
my($this_file);
my($participant_file);
my($script_url);

$debug = 0;
$msw_way = 0;

$participant_name = $ENV{'REMOTE_USER'};
$time_a_place = "kl $msd_time $msd_place";
$msd_list_dir = "modern_self_defense_lists/";
$this_file = "modern_self_defense.cgi";
$participant_file = "msd_participants.txt";
$script_url = "https://inside.axis.com/tools/after_hours/modern_self_defense/modern_self_defense.cgi";
$max_participants = $max_participants - 1;
# Create the CGI object.
my($query)=new CGI; 
my($myself) = $query->self_url;
print $query->header;
print $query->start_html(-title => 'Axis Modern Self Defense', -author => 'stophe@axis.com olak@axis.com');

#my($key);
#&debug_print("Content-type: text/html\n\n");
#foreach $key (keys %ENV) {
#  &debug_print("$key --> $ENV{$key}<br>");
#}

if ($mail_notification == 0)
{
  $message_required = 0;
}
#>>> Check the time >>>
my($time) = time;
my(@time) = localtime($time);
#<<< Check the time <<<


#>>> Get the days and dates we msd>>>
my(@z_days, $z_day, $i);

$i = 0;
while (@z_days < $list_size && $i < 100)
{
  if ($manual_dates == 1)
  {
    $z_day = &next_msd_day_and_date_manual($time + $i * 24*60*60);
  }
  else
  {
    $z_day = &next_msd_day_and_date_auto($time + $i * 24*60*60);
  }
#  &debug_print("$i #" . $z_days[@z_days -1] . "# $z_day @z_days<br>\n");
  if (($i == 0) || ($z_days[@z_days -1] ne $z_day))
  {
    $z_days[@z_days] = $z_day;
#    &debug_print("###" . $z_days[@z_days - 1] . "<br>\n");
  }
  $i++;
}
#<<< Get the days and dates we msd <<<


#>>> Read the input >>>
my(@i_names) = $query->param;
my($i_names) = join("#", @i_names);
my($i_add, $i_name);
&debug_print("$i_names<br>\n");
foreach $i_name (@i_names)
{
  &debug_print($query->param("$i_name") . "#");
}
&debug_print("<br>\n");

if (index($i_names, "add") != -1)
{
  $i_add = $query->param('add'); # 
  &debug_print("add: $i_add<br>\n");
}
else
{
  $i_add = "- Anmäl -";
  &debug_print("add else: $i_add<br>\n");
}
my($i_remove);
if (index($i_names, "remove") != -1)
{
  $i_remove = $query->param('remove'); # 
  &debug_print("rem: $i_remove<br>\n");
}
else
{
 $i_remove = "- Avanmäl -";
 &debug_print("rem else: $i_remove<br>\n");
}

my($i_message);
if (index($i_names, "message") != -1)
{
  $i_message = $query->param('message'); #
  &debug_print("mes: $i_message<br>\n");
}
else
{
  $i_message = "";
  &debug_print("mes else: $i_message<br>\n");
}

my($i_date);
if (index($i_names, "date") != -1)
{
  $i_date = $query->param('date'); #
  &debug_print("dat: $i_date<br>\n");
}
else
{
  $i_date = "";
  &debug_print("dat else: $i_date<br>\n");
}
my($i_new_participant);
if (index($i_names, "new_participant") != -1)
{
  $i_new_participant = $query->param('new_participant'); #
  &debug_print("new: $i_new_participant<br>\n");
}
else
{
  $i_new_participant = "";
  &debug_print("new else: $i_new_participant<br>\n");
}
my($i_old_participant);
if (index($i_names, "old_participant") != -1)
{
  $i_old_participant = $query->param('old_participant'); #
  &debug_print("old: $i_old_participant<br>\n");
}
else
{
  $i_old_participant = "- Ta bort en dansare -";
  &debug_print("old else: $i_old_participant<br>\n");
}
my($i_reminder);
if (index($i_names, "reminder") != -1)
{
  $i_reminder = $query->param('reminder'); #
  &debug_print("reminder: $i_reminder<br>\n");
}
else
{
  $i_reminder = 0;
  &debug_print("reminder else: $i_reminder<br>\n");
}
#<<< Read the input <<<

#>>> Handle inpput >>>
my($file_name, $file, @participant_list, $participant, $date, $day, $t_time);
my($n_participants) = 0;
my($reposted) = 0;
my($no_mess) = 0;
my($full) = 0;
my($removed) = 0;
if ($i_add ne "- Anmäl -")
{
  $file_name = $msd_list_dir . substr($i_date, -8) . ".txt";
  $file = &read_file($file_name);
  @participant_list = split("\n",$file);
  foreach $participant (@participant_list)
  {
    if ($participant eq $i_add)
    {
      $reposted = 1;
    }
    if ($participant eq $msd_instuctor_name)
    {
	$msd_instuctor = 1;
    }
    &debug_print("3<br>\n");
  }
  if ($i_add eq $msd_instuctor_name)
  {
      $msd_instuctor = 1;
  }  
  if ($reposted == 0)
  {
    @participant_list = split("\n",$file);
    $n_participants = @participant_list;
    if (($n_participants < $max_participants + $msd_instuctor) && $i_add ne "- Reminder -")
    {
	$file .= "$i_add\n";
	&debug_print("Add $i_add to $file_name<br>\n");
	&write_file($file_name, $file);
	&debug_print("1<br>\n");
	@participant_list = split("\n",$file);
    }
    elsif ($i_add ne "- Reminder -")
    {
	$full = 1;
    }
  }
  $n_participants = @participant_list;
  if ($i_message ne "" )
  {
    $i_message = "Meddelande från " . $i_add . ":\n" . $i_message . "\n\n";
  }
  &debug_print("2<br>\n");
}

&debug_print("4<br>\n");  

if (($i_remove ne "- Avanmäl -") && (($message_required == 0) || (($message_required == 1) && ($i_message ne ""))))
{
 $file_name = $msd_list_dir . substr($i_date, -8) . ".txt";
 $file = &read_file($file_name);
 @participant_list = split("\n",$file);
 $file = "";
#  &debug_print("Remove $i_remove from $file_name<br>\n");
 foreach $participant (@participant_list)
 {
   &debug_print("$participant <br>\n");
    # Don't insert the lazy participant into the file
   if ($participant ne $i_remove)
   {
     $file .= "$participant\n";
   }
   else
   {
     $removed = 1;
   }
   if ($participant eq $msd_instuctor_name)
   {
     $msd_instuctor = 1;
   }  
 }
 if ($i_remove eq $msd_instuctor_name)
 {
     $msd_instuctor = 0;
 }    
 if ($removed == 0)
 {
     $reposted = 1;
 }
 &write_file($file_name, $file);
 @participant_list = split("\n",$file);
 $n_participants = @participant_list;
 if ($i_message ne "")
 {
   $i_message = "Meddelande från " . $i_remove . ":\n" . $i_message . "\n\n";
 }
}
elsif (($i_remove ne "- Avanmäl -") && ($i_message eq "") && ($message_required == 1))
{
    $no_mess = 1;
}

$date = substr($i_date, -8);
$day =  (split(" ", $i_date))[1];
$t_time = (split(" ", $i_date))[2];

if (($mail_notification == 1) || ($i_reminder == 1) || ($mail_min_participants_achieved == 1))
{
if (($mail_min_participants_achieved == 1) && ($reposted == 0))
{
  if (($removed == 0) && ($n_participants == $min_participants))
  {
	  &send_mail($mail_address,
		     "[msd] $min_participants_achieved_message ($day " . &date_string($date) . " kl $t_time)",
		     "$min_participants_achieved_message\n\n"
		     . "Anmälda:\n\n" .
		     $file .
		     "\nAnmälan:\n$script_url",
		     $mail_address);
  }
#  elsif (($removed == 1) && ($n_participants == $min_participants -1))
#  {
#	  &send_mail($mail_address,
#		     "[msd] Avanmälan till Modern Self Defense! En till behövs! ($day " . &date_string($date) . " kl $t_time)",
#		     "Avanmälan till Modern Self Defense! En till behövs!\n\n"
#		     . "Anmälda:\n\n" .
#		     $file .
#		     "\nAnmälan:\n$script_url",
#		     $mail_address);
#  }
}
if ((($mail_min_participants_achieved == 0) && ($n_participants >= 1) && ($reposted == 0) && ($no_mess == 0) && ($full == 0))
    || (($i_reminder == 1) && ($reposted == 0)))
{
  if ($i_reminder == 1)
  {
    &send_mail($mail_address,
	       "[msd] Glöm inte att anmäla er till Modern Self Defense på $day! (" . 
	       &date_string($date) . " kl $t_time)",
	       "Glöm inte att anmäla er till Modern Self Defense på $day! \n\(" . 
	       &date_string($date) . " kl $t_time)\n\n" . $i_message . "Anmälda:\n\n" .
	       $file .
	       "\nAnmälan:\n$script_url",
	       $mail_address);
  }
  elsif ($n_participants == 1)
  {
      if ($removed == 0)
      {
	  &send_mail($mail_address,
		     "[msd] Glöm inte att anmäla er till Modern Self Defense på $day! (" . 
		     &date_string($date) . " kl $t_time)", 
		     "En anmäld! Minst " . ($min_participants-$n_participants) . " till behövs!\n"
		     . ($max_participants + $msd_instuctor - $n_participants) . " platser kvar!\n\n" . $i_message . "Anmälda (". 
		     ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " . 
		     $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "):\n\n" .
		     $file .
		     "\nAnmälan:\n$script_url",
		     $mail_address);
      }
      else
      {
	  &send_mail($mail_address,
		     "[msd] Anmäl er till Modern Self Defense på $day! (" . 
		     &date_string($date) . " kl $t_time) Fler behövs!", 
		     "En anmäld! Minst " . ($min_participants-$n_participants) . " till behövs!\n"
		     . ($max_participants + $msd_instuctor - $n_participants) . " platser kvar!\n\n" . $i_message . "Anmälda (". 
		     ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " . 
		     $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "):\n\n" .
		     $file .
		     "\nAnmälan:\n$script_url",
		     $mail_address);
      }
  }
  elsif ($n_participants < $min_participants)
  {
      if ($removed == 0)
      {
	  &send_mail($mail_address,
		     "[msd] Bara $n_participants anmälda till Modern Self Defense på $day! (" . 
		     &date_string($date) . " kl $t_time) Fler Behövs!",
		     "$n_participants anmälda! Minst " . ($min_participants-$n_participants) . " till behövs!\n"
		     . ($max_participants + $msd_instuctor - $n_participants) . " platser kvar!\n\n" . $i_message . "Anmälda (".
		     ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " . 
		     $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "):\n\n" .
		     $file .
		     "\nAnmälan:\n$script_url",
		     $mail_address);
     }
     else
     {
	  &send_mail($mail_address,
		     "[msd] Avanmälan till Modern Self Defense på $day! (" . 
		     &date_string($date) . " kl $t_time) Fler Behövs!",
		     "$n_participants anmälda! Minst " . ($min_participants-$n_participants) . " till behövs!\n"
		     . ($max_participants + $msd_instuctor - $n_participants) . " platser kvar!\n\n" . $i_message . "Anmälda (". 
		     ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " . 
		     $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "):\n\n" .
		     $file .
		     "\nAnmälan:\n$script_url",
		     $mail_address);
     }
  }
  elsif (($n_participants == $min_participants) && ($msd_instuctor == 1))
  {
      if ($removed == 0)
      {
	  &send_mail($mail_address,
		     "[msd] $n_participants anmälda! Det blir Modern Self Defense på $day! (" . &date_string($date) . " kl $t_time)",
		     "$n_participants anmälda! Det blir Modern Self Defense!\n"
		     . ($max_participants + $msd_instuctor - $n_participants) . " platser kvar!\n\n" . $i_message . "Anm&ouml;lda (". 
		     ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " .
		     $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "):\n\n" .
		     $file .
		     "\nAnm&ouml;lan:\n$script_url",
		     $mail_address);
      }
      else
      {
	  &send_mail($mail_address,
		     "[msd] Avanmälan till Modern Self Defense på $day (" . &date_string($date) . " kl $t_time)",
		     "$n_participants anmälda!\n"
		     . ($max_participants + $msd_instuctor - $n_participants) . " platser kvar!\n\n" . $i_message . "Anmälda (". 
		     ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " .
		     $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "):\n\n" .
		     $file .
		     "\nAnmälan:\n$script_url",
		     $mail_address);
      }
  }
  elsif (($n_participants == $min_participants) && ($msd_instuctor == 0))
  {
      if ($removed == 0)
      {
	  &send_mail($mail_address,
		     "[msd] $n_participants anmälda! Ingen msd instruktör! (" . &date_string($date) . " kl $t_time)",
		     "$n_participants anmälda! Ingen msd instruktör\n"
		     . ($max_participants + $msd_instuctor - $n_participants) . " platser kvar!\n\n" . $i_message . "Anmälda (".
		     ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " .
		     $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "):\n\n" .
		     $file .
		     "\nAnmälan:\n$script_url",
		     $mail_address);
      }
      elsif($i_remove eq $msd_instuctor_name)
      {
	  &send_mail($mail_address,
		     "[msd] Avanmälan till Modern Self Defense på $day (" . &date_string($date) . " kl $t_time)",
		     "$n_participants anmälda! Ingen msd instruktör!\n"
		     . ($max_participants + $msd_instuctor - $n_participants) . " platser kvar!\n\n" . $i_message . "Anmälda (".
		     ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " .
		     $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "):\n\n" .
		     $file .
		     "\nAnmälan:\n$script_url",
		     $mail_address);
      }
      else
      {
	  &send_mail($mail_address,
		     "[msd] Avanmälan till Modern Self Defense på $day (" . &date_string($date) . " kl $t_time)",
		     "$n_participants anmälda!\n"
		     . ($max_participants + $msd_instuctor - $n_participants) . " platser kvar!\n\n" . $i_message . "Anmälda (".
		     ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " .
		     $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "):\n\n" .
		     $file .
		     "\nAnmälan:\n$script_url",
		     $mail_address);
      }
  }  
  elsif ($n_participants == ($max_participants + $msd_instuctor - 1))
  {
      if (($removed == 0) && ($i_add eq $msd_instuctor_name))
      {
	  &send_mail($mail_address,
		     "[msd] Fler anmälda! Det blir Modern Self Defense på $day! (" . &date_string($date) . " kl $t_time)",
		     "$n_participants anmälda! Det blir Modern Self Defense!\nEn plats kvar!\n\n" . $i_message . "Anmälda (".
		     ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " .
		     $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "):\n\n" .
		     $file .
		     "\nAnmälan:\n$script_url",
		     $mail_address);
      }
      if ($removed == 0)
      {
	  &send_mail($mail_address,
		     "[msd] Fler Anmälda till Modern Self Defense på $day! (" . &date_string($date) . " kl $t_time)",
		     "$n_participants anmälda!\nEn plats kvar!\n\n" . $i_message . "Anmälda (".
		     ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " .
		     $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "):\n\n" .
		     $file .
		     "\nAnmälan:\n$script_url",
		     $mail_address);
      }
      elsif($i_remove eq $msd_instuctor_name)
      {
	  &send_mail($mail_address,
		     "[msd] Avanmälan till Modern Self Defense på $day (" . &date_string($date) . " kl $t_time)",
		     "$n_participants anmälda! Ingen msd instruktör!\nEn plats kvar!\n\n" . $i_message . "Anmälda (".
		     ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " .
		     $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "):\n\n" .
		     $file .
		     "\nAnmälan:\n$script_url",
		     $mail_address);
      }
      else
      {
	  &send_mail($mail_address,
		     "[msd] Avanmälan till Modern Self Defense på $day (" . &date_string($date) . " kl $t_time)",
		     "$n_participants anmälda!\nEn plats kvar!\n\n" . $i_message . "Anmälda (".
		     ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " .
		     $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "):\n\n" .
		     $file .
		     "\nAnmälan:\n$script_url",
		     $mail_address);
      }
  }  
  elsif ($n_participants < $max_participants + $msd_instuctor)
  {
      if (($removed == 0) && ($i_add eq $msd_instuctor_name))
      {
	  &send_mail($mail_address,
		     "[msd] Fler anmälda! Det blir Modern Self Defense på $day! (" . &date_string($date) . " kl $t_time)", 
		     "$n_participants anmälda! Det blir Modern Self Defense!\n"
		     . ($max_participants + $msd_instuctor - $n_participants) . " platser kvar!\n\n" . $i_message . "Anmälda (". 
		     ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " .
		     $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "):\n\n" .
		     $file .
		     "\nAnmälan:\n$script_url",
		     $mail_address);
      }
      elsif ($removed == 0)
      {
	  &send_mail($mail_address,
		     "[msd] Fler Anmälda till Modern Self Defense på $day! (" . &date_string($date) . " kl $t_time)",
		     "$n_participants anmälda!\n"
		     . ($max_participants + $msd_instuctor - $n_participants) . " platser kvar!\n\n" . $i_message . "Anmälda (".
		     ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " .
		     $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "):\n\n" .
		     $file .
		     "\nAnmälan:\n$script_url",
		     $mail_address);
      }
      elsif($i_remove eq $msd_instuctor_name)
      {
	  &send_mail($mail_address,
		     "[msd] Avanmälan till Modern Self Defense på $day (" . &date_string($date) . " kl $t_time)",
		     "$n_participants anmälda! Ingen msd instruktör!\n"
		     . ($max_participants + $msd_instuctor - $n_participants) . " platser kvar!\n\n" . $i_message . "Anmälda (".
		     ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " .
		     $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "):\n\n" .
		     $file .
		     "\nAnmälan:\n$script_url",
		     $mail_address);
      }
      else
      {
	  &send_mail($mail_address,
		     "[msd] Avanmälan till Modern Self Defense på $day (" . &date_string($date) . " kl $t_time)",
		     "$n_participants anmälda!\n"
		     . ($max_participants + $msd_instuctor - $n_participants) . " platser kvar!\n\n" . $i_message . "Anmälda (". 
		     ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " .
		     $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "):\n\n" .
		     $file .
		     "\nAnmälan:\n$script_url",
		     $mail_address);
      }
  }
  elsif ($n_participants == $max_participants + $msd_instuctor)
  {
      if ($i_add eq $msd_instuctor_name)
      {
	  &send_mail($mail_address,
		     "[msd] Fullt på Modern Self Defense! Det blir Modern Self Defense på $day! (" . &date_string($date) . " kl $t_time)",
		     "$n_participants anmälda! Det blir Modern Self Defense!\nFullt!\n\n" . $i_message . "Anmälda (".
		     ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " .
		     $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "):\n\n" .
		     $file .
		     "\nAnmälan:\n$script_url",
		     $mail_address);
      }
      else
      {
	  &send_mail($mail_address,
		     "[msd] Fullt på Modern Self Defense på $day! (" . &date_string($date) . " kl $t_time)",
		     "$n_participants anmälda!\nFullt!\n\n" . $i_message . "Anmälda (". 
		     ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " .
		     $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "):\n\n" .
		     $file .
		     "\nAnmälan:\n$script_url",
		     $mail_address);
      }
  }
    
}
elsif (($n_participants == 0) && ($removed == 1))
{
    &send_mail($mail_address,
               "[msd] Avanmälan till Modern Self Defense på $day! (" . 
               &date_string($date) . " kl $t_time) Ingen Anmäld!", 
	       "Anmäl er till modern self defense! \n" . ($max_participants + $msd_instuctor - $n_participants) . " platser kvar!\n\n" . $i_message . "Anmälda (". 
	       ($time[5] + 1900) . "-" . &pad_number($time[4] + 1) . "-" . &pad_number($time[3]) . " " . 
	       $time[2] . ":" . &pad_number($time[1]) . ":" . &pad_number($time[0]) . "): Ingen! \n\nAnmälan:\n$script_url",
               $mail_address);
}


if ($reposted == 0)
{

    if ($no_mess == 1)
    {
	print "<font color=\"red\">För att kunna avanmäla sig måste ett meddelande med orsaken till Avanmälan anges!</font><br>\n";
    }
    elsif ($full == 1)
    {
	print "<font color=\"red\">Tyvärr är det redan fullt på modern self defense på $i_date.</font><br>\n";
    }
    elsif ($i_reminder == 1)
    {
	print "<font color=\"blue\">Ett email har skickats till" .
	    " $mail_address som påminnelse för $i_date.</font><br>\n";
    }
    elsif ($mail_min_participants_achieved == 1)
    {
    }
    elsif ($removed == 1)
    {
	print "<font color=\"blue\">Ett email har skickats till" .
	    " $mail_address om din Avanmälan på $i_date.</font><br>\n";
    }
    elsif ($n_participants >= 1)
    {
	print "<font color=\"blue\">Ett email har skickats till" .
	    " $mail_address om din Anmälan på $i_date.</font><br>\n";
    }
}
}

if (($mail_notification == 0) && ($reposted == 0))
{

    if ($no_mess == 1)
    {
	print "<font color=\"red\">För att kunna avanmäla sig måste ett meddelande med orsaken till Avanmälan anges!</font><br>\n";
    }
}

$reposted = 0;
$no_mess = 0;
$full = 0;
$removed = 0;
if ($i_new_participant ne "")
{
  $file = &read_file($participant_file);
  @participant_list = split("\n",$file);
  foreach $participant (@participant_list)
  {
    if ($participant eq $i_new_participant)
    {
      $reposted = 1;
    }
  }
  if ($reposted == 0)
  {
    $file .= "$i_new_participant\n";
    &debug_print("Add new participant $i_add to $participant_file<br>\n");
    &write_file($participant_file, $file);
  }
}
if ($i_old_participant ne "- Ta bort en dansare -")
{
  $file = &read_file($participant_file);
  @participant_list = split("\n",$file);
  $file = "";
  &debug_print("Remove $i_old_participant from $participant_file<br>\n");
  foreach $participant (@participant_list)
  {
    &debug_print("$participant <br>\n");
    # Don't insert the old participant into the file
    if ($participant ne $i_old_participant)
    {
      $file .= "$participant\n";
    }
  }
  &write_file($participant_file, $file);
}
#<<< Handle inpput <<<

#>>> Print information >>>
my($d);

if ($show_user_pic == 1)
{

#if (-e "msd_pics/$participant_name.jpg")
#{
#print "<a href=\"http://galaxis.axis.com/people/".$participant_name."/default.aspx\"><img src=\"msd_pics/".$participant_name.".jpg\" border=\"0\"></a>";
#}
#else
#{
print "<a href=\"http://galaxis2013.axis.com/mysite/Person.aspx?accountname=AXISNET%5C".$participant_name."\"><img src=\"http://galaxis2013.axis.com/mysite/User Photos/Profile Pictures/".$participant_name."_LThumb.jpg\" border=0 width=96 height=96></a>";
#}
}

if ($manual_dates == 1)
{
print "<h2>$msd_name ";
print $msd_place . "</h2>\n";
}
else
{
print "<h2>$msd_name på ";
print $msd_day . "ar kl 17:00-18:00 och " . $msd_day2 . "ar kl 16:30-17:30 " . "</h2>\n";
}

# , Men INTE:&nbsp;";
# foreach $d (@no_msd_dates)
# {
#   print $d . ",&nbsp;";
# }
#  print "<br>\n";
print "<hr>\n";


#<<< Print information <<<

#>>> Print the lists >>>
#my(@lazy_list, $lazy);
my($participants) = &read_file($participant_file);
my(@participants) = split("\n",$participants);
my($next_week) = 0;
my($added) = 0;
my($b_time);
my($n_date);
my($participant_pic);
my($size)

 &debug_print("Print the lists:<br>\n");


foreach $z_day (@z_days)
{
  $added = 0;
  $date = substr($z_day, -8);
  $n_date = (split(" ", $z_day))[0];
  $day =  (split(" ", $z_day))[1];
  $b_time = (split(" ", $z_day))[2];
#  print "<h4>" . $day . " " . &date_string($date) . "</h4>\n";
  print "<h4>" . $day . " " . &date_string($date) . " kl " . $b_time . "</h4>\n";
  $file_name = $msd_list_dir . $date . ".txt";
#  &debug_print($file_name . "<br>\n");
  $file = &read_file($file_name);
  @participant_list = split("\n",$file);
#  @lazy_list = @participants;
  $n_participants = @participant_list;

  if ($n_date == 1)
  {
    print "$no_msd_message<br>\n<br>\n";

#    print "<h2><font color=\"red\">GOD JUL & GOTT NYTT �R!</font></h2>\n";

  }
  else
  {
    
  foreach $participant (@participant_list)
  {
      if ($participant eq $msd_instuctor_name)
      {
	  $msd_instuctor = 1;
      }

      if ($participant eq $participant_name)
      {
          $added = 1;
      } 
  }
  
#  print "<font color=\"red\">OBS</font>! Max " . ($max_participants) . " dansare + msd instruktör!<br>\n";
#  print "<br>\n";

if ($n_date == 0)
{
  
  if($n_participants == 0)
  {
      print "Ingen Anmäld! <br>\n"; # . ($max_participants + $msd_instuctor - $n_participants) . " platser kvar!<br>\n";
  }
  elsif($n_participants == 1)
  {
      print "En Anmäld! <font color=\"red\">Minst " . ($min_participants - $n_participants) . " till behövs</font>!<br>\n"; # . ($max_participants + $msd_instuctor - $n_participants) . " platser kvar!<br>\n";
  }
  elsif($n_participants < $min_participants)
  {
      print "$n_participants anmälda! <font color=\"red\">Minst " . ($min_participants - $n_participants) . " till behövs</font>!<br>\n" # . ($max_participants + $msd_instuctor - $n_participants) . " platser kvar!<br>\n";
  }
  elsif($n_participants == ($max_participants + $msd_instuctor - 1))
  {
      print "$n_participants anmälda! ";
      if($msd_instuctor == 1)
      {
	  print "<font color=\"blue\">Det blir Modern Self Defense!</font><br>\n";
      }
      else
      {
	  print "<font color=\"red\">Ingen msd instruktör!</font><br>\n";
      }
      print "<font color=\"red\">En plats kvar</font>!<br>\n";
  }  
  elsif($n_participants < ($max_participants + $msd_instuctor))
  {
      print "$n_participants anmälda! ";
      if($msd_instuctor == 1)
      {
	  print "<font color=\"blue\">Det blir Modern Self Defense!</font> <br>\n";
      }
      else
      {
	  print "<font color=\"red\">Ingen msd instruktör!</font> <br>\n";
      }
      print "" . ($max_participants + $msd_instuctor - $n_participants) . " platser kvar!<br>\n";
  }
  elsif($n_participants >= ($max_participants + $msd_instuctor))
  {
      print "$n_participants anmälda! ";
      if($msd_instuctor == 1)
      {
	  print "<font color=\"blue\">Det blir Modern Self Defense!</font> <br>\n";
      }
      else
      {
	  print "<font color=\"red\">Ingen msd instruktör!</font> <br>\n";
      }
      print "<font color=\"red\">Fullt</font>!<br>\n";
  }

  print "<br>\n";

}

  if (!$added)
  {
    print "<form method=\"post\" action=\"$this_file\">";
    print "<input type=\"submit\" value=\"Jag vill anmäla mig!\">";
    if ($mail_notification == 1)
    {
      print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Meddelande: ";
      print "<input type=\"edit\" name=\"message\" value=\"\">";
    }
    print "<input type=\"hidden\" name=\"add\" value=\"$participant_name\">";
    print "<input type=\"hidden\" name=\"date\" value=\"$z_day\">";
    print "</form>";
  }
  else
  {
    print "<form method=\"post\" action=\"$this_file\">";
    print "<input type=\"submit\" value=\"Jag vill avanmäla mig!\">";
    if ($mail_notification == 1)
    {
      print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Meddelande: ";
      print "<input type=\"edit\" name=\"message\" value=\"\">";
    }
    print "<input type=\"hidden\" name=\"remove\" value=\"$participant_name\">";
    print "<input type=\"hidden\" name=\"date\" value=\"$z_day\">";
    print "</form>";
  }

  if (($mail_reminder == 1) && ($participant_name eq $msd_instuctor_name))  
  {
    print "<form method=\"post\" action=\"$this_file\">";
    print "<input type=\"submit\" value=\"Skicka p&aring;minnelse\">";
    print "<input type=\"hidden\" name=\"add\" value=\"- Reminder -\">";
    print "<input type=\"hidden\" name=\"date\" value=\"$z_day\">";
    print "<input type=\"hidden\" name=\"reminder\" value=\"1\">";
    print "</form>";
  }

  if($n_participants > 0)
  {
  print "<h4>\n Anmälda:</h4>\n";
  }
}

if ($n_date == 0)
{
  
  foreach $participant (@participant_list)
  {
    print "$participant <br>\n";
    # Remove from the lazy list
    #$i = 0;
    #while ($i < @lazy_list)
    #{
    #  $lazy = $lazy_list[$i];
    #  if ($lazy eq $participant)
    #  {
    #    splice(@lazy_list, $i, 1);
    #    $i = @lazy_list; # End the search
    #  }
    #$i++;
    #}
  }

  print "<br>\n";
}
#  if ($next_week == 0)
#  {
#
#  print "<form method=\"post\" action=\"$this_file\">";
#  # Droplist for lazy:
#  print "<select name=\"add\">\n";
#  print "<option>- Anmäl -</option>\n";
#  foreach $lazy (@lazy_list)
#  {
#    print "<option>$lazy</option>\n";
#  }
#  print "</select>";
#  # Droplist for not lazy:
#  print "<select name=\"remove\">\n";
#  print "<option>- AvAnmäl -</option>\n";
#  foreach $participant (@participant_list)
#  {
#    print "<option>$participant</option>\n";
#  }
#  print "</select>";
#    
#  # Do it button and hidden date
#  print "<input type=\"submit\" value=\"Utf�r!\">";
#  print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Meddelande: ";
#  print "<input type=\"edit\" name=\"message\" value=\"\">";
#  print "<input type=\"hidden\" name=\"date\" value=\"$z_day\">";
#  print "</form>";
#  print "<hr>\n";
#  }
#  else
#  {
  # Do it button and hidden date

  if ($show_participants_pic == 1)
  {
    foreach $participant (@participant_list)
    {
	print "<a href=\"http://galaxis2013.axis.com/mysite/Person.aspx?accountname=AXISNET%5C".$participant."\"><img src=\"http://galaxis2013.axis.com/mysite/User Photos/Profile Pictures/".$participant."_LThumb.jpg\" border=0 width=96 height=96></a>";
    }
  }

#  }
#  }
  print "<hr>\n";

  $next_week++;
}

#<<< Print the lists <<<


#>>> Print admin section >>>
#  print "<form method=\"post\" action=\"$this_file\">";
#  print "<h4> Administration </h4>\n";
#  print "L�gg till en ny dansare:&nbsp;";  
#  print "<input type=\"edit\" name=\"new_participant\" value=\"\">";
#  print "&nbsp;";

  # Droplist for all participants:
#  print "<select name=\"old_participant\">\n";
#  print "<option>- Ta bort en dansare -</option>\n";
#  foreach $participant (@participants)
#  {
#    print "<option>$participant</option>\n";
#  }
#  print "</select>";
#  print "<input type=\"submit\" value=\"Utf�r!\">";
#  print "</form>";
#<<< Print admin section <<<


#>>> Print stat link >>>
#  print "<hr>\n";
if ($show_statistics == 1) {
  print "<a HREF=\"modern_self_defense_stat.cgi\">Statistik</a>";
}
#<<< Print stat link <<<

print $query->end_html, "\n";

sub next_msd_day_and_date_auto()
{
  my($search_time) = $_[0];
  my(@time);
  my($day);
  my($date) = "";
  my($no_date);
  my($week);
  my($count);
  my($cancel) = 0;
  
  # Return date of next msd.
#  &debug_print("Start: $search_time<br>\n");
  while ($date eq "")
  {
#    &debug_print("$search_time<br>\n");
    @time = localtime($search_time);
    $day = &week_day($time[6]);
    $week = (((($time[4] * 30 + $time[3] - 1) / 7) + 1) & 1);
#    print "$time[4] * 30 + $time[3] - 3) / 7) + 1) & 1 = $week\n";
#    &debug_print("$day<br>\n");
    if (($day eq $msd_day)
        or ($day eq $msd_day2))
    {
      if (($day eq $msd_day))
      {
        $date = $day . " " . $msd_time . " " . ($time[5] + 1900) .
              sprintf("%02d", $time[4] + 1) .
              sprintf("%02d", $time[3]);

      } else {
        $date = $day . " " . $msd_time2 . " " . ($time[5] + 1900) .
              sprintf("%02d", $time[4] + 1) .
              sprintf("%02d", $time[3]);
      
      }
      $count = 0;
      foreach $no_date (@no_msd_dates)
      {
#        &debug_print("Test $date for no_date:$no_date<br>\n");
        if (index($no_date,"-") == -1)
        {
	  if (index($date, $no_date) != -1)
	  {
            &debug_print("Found in $no_date #1<br>\n");
#            $date = $new_msd_days[$count] . " " . $new_msd_times[$count] . " " . $new_msd_dates[$count];
#	    $msd_time = $new_msd_times[$count];
            $cancel = 1;
          }
        }
	else
        {

#          &debug_print(substr($date, -8) . "###" . substr($no_date, 0, 8) . "###" . substr($no_date, -8) . "<br>\n");
          if (substr($date, -8) ge substr($no_date, 0, 8))
          {
#            &debug_print("#<br>\n");
            if (substr($date, -8) le substr($no_date, -8))
            {
#              &debug_print("Found in $no_date #2<br>\n");
#              $date = $new_msd_days[$count] . " " . $new_msd_times[$count] . " " . $new_msd_dates[$count];
#	      $msd_time = $new_msd_times[$count];
              $cancel = 1;
            }
          }
        }
        $count++;
      }
      $date = $cancel . " " . $date;
    }

    $search_time += 24*60*60; # Add 1 day in seconds.
  }
#  print("End: $date<br><br>\n\n");
  return $date;
}

sub next_msd_day_and_date_manual()
{
  my($search_time) = $_[0];
  my(@time);
  my($day);
  my($date) = "";
  my($msd_date);
  my($week);
  my($count);
  my($found);
  my($days) = 0;
  
  # Return date of next msd.
#  &debug_print("Start: $search_time<br>\n");
  while ($date eq "" && $days < 100)
  {
#    &debug_print("$search_time<br>\n");
    @time = localtime($search_time);
    $day = &week_day($time[6]);
    $week = (((($time[4] * 30 + $time[3] - 1) / 7) + 1) & 1);
#    print "$time[4] * 30 + $time[3] - 3) / 7) + 1) & 1 = $week\n";
#    &debug_print("$day<br>\n");
      $date = ($time[5] + 1900) .
              sprintf("%02d", $time[4] + 1) .
              sprintf("%02d", $time[3]);
      $count = 0;
      $found = 0;
      foreach $msd_date (@msd_dates)
      {
#        &debug_print("Test $date for no_date:$no_date<br>\n");
        if (index($msd_date,"-") == -1)
        {
	  if (index($date, $msd_date) != -1)
	  {
#            &debug_print("Found in $no_date #1<br>\n");
#            $date = $new_msd_days[$count] . " " . $new_msd_times[$count] . " " . $new_msd_dates[$count];
#	    $msd_time = $new_msd_times[$count];
	    $date = $day . " " . $msd_times[$count] . " " . $date;
            $found = 1;
          }
        }
	else
        {

#          &debug_print(substr($date, -8) . "###" . substr($no_date, 0, 8) . "###" . substr($no_date, -8) . "<br>\n");
          if (substr($date, -8) ge substr($msd_date, 0, 8))
          {
#            &debug_print("#<br>\n");
            if (substr($date, -8) le substr($msd_date, -8))
            {
#              &debug_print("Found in $no_date #2<br>\n");
#              $date = $new_msd_days[$count] . " " . $new_msd_times[$count] . " " . $new_msd_dates[$count];
#	      $msd_time = $new_msd_times[$count];
	      $date = $day . " " . $msd_times[$count] . " " . $date;
              $found = 1;
            }
          }
        }
        $count++;
      }
      if ($found == 0)
      {
	$date = "";
      }
      else
      {
	$date = "0" . " " . $date;
      }
    $search_time += 24*60*60; # Add 1 day in seconds.
    $days++;
  }
#  print("End: $date<br><br>\n\n");
  return $date;
}

sub pad_number {
  my($number_to_pad) = $_[0];
  if ($number_to_pad < 10)
  {
    return "0" . $number_to_pad;
  }
  else
  {
    return "" . $number_to_pad;
  }
}

sub week_day
{
  my($aNumber) = $_[0];

  if ($aNumber == 1)
  {
    return "Måndag";
  }
  elsif ($aNumber == 2)
  {
    return "Tisdag";
  }
  elsif ($aNumber == 3)
  {
    return "Onsdag";
  }
  elsif ($aNumber == 4)
  {
    return "Torsdag";
  }
  elsif ($aNumber == 5)
  {
    return "Fredag";
  }
  elsif ($aNumber == 6)
  {
    return "Lördag";
  }
  elsif ($aNumber == 0)
  {
    return "Söndag";
  }
  else 
  {
    return "???dag";
  }
}

sub month_string
{
  my($aNumber) = $_[0];

  if ($aNumber == 1)
  {
    return "Januari";
  }
  elsif ($aNumber == 2)
  {
    return "Februari";
  }
  elsif ($aNumber == 3)
  {
    return "Mars";
  }
  elsif ($aNumber == 4)
  {
    return "April";
  }
  elsif ($aNumber == 5)
  {
    return "Maj";
  }
  elsif ($aNumber == 6)
  {
    return "Juni";
  }
  elsif ($aNumber == 7)
  {
    return "Juli";
  }
  elsif ($aNumber == 8)
  {
    return "Augusti";
  }
  elsif ($aNumber == 9)
  {
    return "September";
  }
  elsif ($aNumber == 10)
  {
    return "Oktober";
  }
  elsif ($aNumber == 11)
  {
    return "November";
  }
  elsif ($aNumber == 12)
  {
    return "December";
  }
  else 
  {
    return "???månad";
  }
}

sub date_string
{
  my($date) = $_[0];
  my($year) = substr($date, 0, 4);
  my($month) = &month_string(substr($date, 4, 2));
  my($day) = substr($date, 6, 2);
  return "$day $month $year";
}

sub read_file {
  my($file_name) = $_[0];
  my($file_text) = "";
  my($file_line) = "";


#  &debug_print("read_file $file_name\n");

  if (!(-e $file_name))
  {
    return "";
  }

  open(AFILE, "$file_name") or
	die "Could not open $file_name: $!";
  if ($msw_way == 1)
  {
    binmode(AFILE, ":raw");
  }
  while (defined($file_line = <AFILE>))
  {
#	&debug_print("#$file_text#");
	$file_text .= $file_line;
  }
  close(AFILE);
  return $file_text;
}

sub write_file {
  my($file_name) = $_[0];
  my($file_text) = $_[1];

#  &debug_print("write_file $file_name\n#$file_text#");
  open(AFILE, ">$file_name") or
	die "Could not open $file_name: $!";
  if ($msw_way == 1)
  {
    binmode(AFILE, ":raw");
  }
  print AFILE $file_text;
  close(AFILE);
}

sub send_mail {
    my($receiver) = $_[0];
    my($subject) = $_[1];
    my($message) = $_[2];
    my($sender) = $_[3];
    my($msg);
    
    &debug_print("Send mail to $receiver\n");

    $msg = new MIME::Lite;

    $msg->build(Type => "TEXT",
                Data => "$message");
    $msg->add(From => $sender);
    $msg->add(Subject => $subject);
#    $msg->add(Cc => $opt_C);
    $msg->add(To => $receiver);
    $msg->send;
}

sub debug_print
{
  my($text) = $_[0];
  if ($debug)
  {
    print "$text";
  }
}


exit 0;
