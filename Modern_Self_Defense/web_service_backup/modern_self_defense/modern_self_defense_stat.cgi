#!/usr/bin/perl

use strict;
use CGI;
use MIME::Lite;

my($debug);
my($msw_way);
my($game_list_dir);
my($this_file);
my(@game_file_names);
my(@first_dates);
my($first_date);
my($last_date);
my($time);
my(@time);
my($game_file_name, @valid_file_names);
my(@i_names);
my($i_names);
my($i_add, $i_name);
my($start_date, $date, $file, @players, $player);
my(%s_player, %s_players);
my($pass);
my($no_pass);
my($n_players);
my(@keys);
my($key, @player_list);
my($np);
my(@players_list);
my($nps);
my($i);
my($i_date);

$debug = 0;
$msw_way = 0;
$game_list_dir = "modern_self_defense_lists/";
$this_file = "modern_self_defense_stat.cgi";
$first_dates[0] = 20110224;

# Create the CGI object.
my($query)=new CGI; 
my($myself) = $query->self_url;
print $query->header;
print $query->start_html(-title => 'Modern Self Defense Statistik', -author => 'stophe@axis.com olak@axis.com');

#my($key);
#&debug_print("Content-type: text/html\n\n");
#foreach $key (keys %ENV) {
#  &debug_print("$key --> $ENV{$key}<br>");
#}


#>>> Check the time >>>
$time = time;
@time = localtime($time);
#<<< Check the time <<<

$last_date = ($time[5] + 1900) .
              sprintf("%02d", $time[4] + 1) .
              sprintf("%02d", $time[3]);

#>>> Read valid file names >>>
@game_file_names = &read_file_names($game_list_dir);

foreach $first_date (@first_dates)
{

@valid_file_names = 0;

foreach $game_file_name (@game_file_names)
{
#  &debug_print("$game_file_name " . substr($game_file_name, 0, 8) . "<br>\n");
  if (length($game_file_name) == 12)
  {

    if (substr($game_file_name, -4) eq ".txt")
    {
      if (substr($game_file_name, 0, 8) >= $first_date)
      {
	if (substr($game_file_name, 0, 8) < $last_date)
	{
#         &debug_print(">>>>>>> $game_file_name<br>\n");
	  push(@valid_file_names, substr($game_file_name, 0 , 8));
        }
      }
    }
  }
}
@valid_file_names = sort(@valid_file_names);
#<<< Read valid file names <<<


#>>> Read the input >>>
@i_names = $query->param;
$i_names = join("#", @i_names);
&debug_print("$i_names<br>\n");
foreach $i_name (@i_names)
{
  &debug_print($query->param("$i_name") . "#");
}
&debug_print("<br>\n");

if (index($i_names, "start_date") != -1)
{
  $i_date = $query->param('start_date');
  &debug_print("start_date: $i_date<br>\n");
}
else
{
  $i_date = "- Nytt startdatum -";
  &debug_print("dat else: $i_date<br>\n");
}
#<<< Read the input <<<

#>>> Handle inpput >>>
if ($i_date eq "- Nytt startdatum -")
{
  $start_date = $valid_file_names[0];
}
else
{
  $start_date = $i_date;
}

# Read stat
$pass = 0;
$no_pass = 0;
%s_player = "";
%s_players = "";;
foreach $date (@valid_file_names)
{
  if ($date >= $start_date)
  {
    &debug_print("$date<br>\n");
    $file = read_file($game_list_dir . $date . ".txt");
    @players = split("\n", $file);
    $n_players = @players;
    if ($n_players > 7)
    {
      foreach $player (@players)
      {
        &debug_print("&nbsp;&nbsp;$player<br>\n");
        if (exists($s_player{$player}))
        {
          $s_player{$player} = $s_player{$player} + 1;
        }
        else
        {
          $s_player{$player} = 1;
        }
      }
      $s_players{@players . " deltagare"} = $s_players{@players . " deltagare" } + 1;
      $pass++;
    }
    else
    {
      $no_pass++;
    }
  }
}

# Create lists
@keys = keys(%s_player);
$np = 0;
foreach $key (@keys)
{
  #print "&nbsp;&nbsp;&nbsp; $key: " . $s_player{$key} .  "<br>\n";i
  $player_list[$np] = $s_player{$key} . " " . $key;
  $np++;
}
@player_list = sort {$a <=> $b} (@player_list);

@keys = keys(%s_players);
$nps = 0;
foreach $key (@keys)
{
  #print "&nbsp;&nbsp;&nbsp; $key: " . $s_players{$key} .  "<br>\n";i
  $players_list[$nps] =  $key . ": " . $s_players{$key};
  $nps++;
}
@players_list = sort {$a <=> $b} @players_list;
#<<< Handle inpput <<<

#>>> Print information >>>
print "<h2>Modern Self Defense Statistik</h2>\n";
print "<h4>Totalt antal pass sedan $first_date:</h4>\n";
print "&nbsp;&nbsp;&nbsp$pass pass<br>\n";
print "<br>\n";
print "<hr>\n";
print "<br>\n";
print "<h4>Antal pass med:</h4>\n";
$i = 0;
while ($i < $nps)
{
  print "&nbsp;&nbsp;&nbsp;" . $players_list[$nps - 1 - $i] .  "<br>\n";
  $i++;
}
print "<hr>\n";
print "<h4>Antal pass per deltagare:</h4>\n";
$i = 0;
while ($i < $np)
{
  print "&nbsp;&nbsp;&nbsp;" . $player_list[$np - 1 - $i] .  "<br>\n";
  $i++;
}
print "<hr>\n";
print "<br>\n";
#print "&nbsp;&nbsp;&nbsp; för lite deltagare: " . $no_pass .  "<br>\n";
#print "<br>\n";
#print "<hr>\n";

}

#print "<h4>Adminstration:</h4>\n";

#<<< Print information <<<


#>>> Print the lists >>>
#&debug_print("Print the lists:<br>\n");
#print "<form method=\"post\" action=\"$this_file\">";

# Droplist for start date:
#my($list_date);
#print "<select name=\"start_date\">\n";
#print "<option>- Nytt startdatum -</option>\n";
#foreach $list_date (@valid_file_names)
#{
#  print "<option>$list_date</option>\n";
#}
#print "</select>";

# Do it button and hidden date
#print "<input type=\"submit\" value=\"Utför!\">";
#print "</form>";
#print "<hr>\n";
#<<< Print the lists <<<

#>>> Print stat link >>>
print "<a HREF=\"modern_self_defense.cgi\">Anmälan</a>";
#<<< Print stat link <<<

print $query->end_html, "\n";

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

sub pad_number {
  my($number_to_pad) = $_[0];
  if ($number_to_pad < 10)
  {
    return "&nbsp;&nbsp;" . $number_to_pad;
  }
  else
  {
    return "" . $number_to_pad;
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


sub read_file_names {
my($dir_name) = $_[0];
my(@file_names);
my($file_name) = "";

&debug_print("read_file $dir_name<br>\n");

opendir(ADIR, "$dir_name") or
die "Could not open $dir_name: $!";
while (defined($file_name = readdir(ADIR)))
{
#    &debug_print("???: $file_name#<br>\n");
if (-f $dir_name . "/$file_name")
{
#      &debug_print("f: $file_name#<br>\n");
push(@file_names, $file_name);
}
}
closedir(ADIR);
return @file_names;
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
