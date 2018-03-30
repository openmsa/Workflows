##########################################################
#
# 実行方法    : perl henkan.pl [ファイルパス]
#               (例) perl henkan.pl /root/test.sql
#
# 仕様        : SQL文のvaluesにあるJSON形式をエスケープする
#               実行結果は入力ファイルと同じ場所にファイル名
#               の最初に OUT_ を付加して作成する
#
##########################################################

use strict;
use warnings;

# 定数
use constant DELI_F => "\"{";
use constant DELI_L => "}\"";
use constant DELI_VALIUES => "values";
use constant PRE_OUTFILE => "OUT_";

# 引数の入力ファイルパスを取得
my $file_in = shift;

open(my $fh_in, "< " . $file_in) or die("Error:$!");

# 入力ファイル全体を読み込む
my $content = do { local $/; <$fh_in> };

close($fh_in);

# 出力用文字列
my $output = "";

# SQL文の「values」までは改行コードを残す
my $wkText = $content;
my $pos = index($wkText, DELI_VALIUES);
if ($pos > 0) {
	$output = substr($wkText, 0, $pos);
	$output .= DELI_VALIUES . "\r\n";
	$wkText = substr($wkText, $pos + 6);
}

# 改行コード、TABコードを削除する
$wkText =~ s/\t//g;
$wkText =~ s/\r//g;
$wkText =~ s/\n//g;

# 最初の "{ と }" の位置を取得する
my $first = index($wkText, DELI_F);
my $last  = index($wkText, DELI_L);

# 作業用文字列
my $tmpText = "";

while ($first > 0) {
	# ),( のカンマの後ろに改行コードを挿入
	$wkText =~ s/\)\,\(/\)\,\r\n\(/g;
	$output .= substr($wkText, 0, $first);
	$tmpText = substr($wkText, $first + 2, $last - $first - 2);
	$output .= DELI_F;

	# ダブルクォーテーション、スラッシュをエスケープする
	$tmpText =~ s/\"/\\\\\"/g;
	$tmpText =~ s/\//\\\\\\\//g;

	$output .= $tmpText;
	$output .= DELI_L;
	$wkText = substr($wkText, $last + 2);

	# 次の "{ と }" の位置を取得する
	$first = index($wkText, DELI_F);
	$last  = index($wkText, DELI_L);
}

# 最後の文字列を連結する
$output .= $wkText;

# 出力ファイル名の生成
my $file_out = $file_in;
$pos = rindex($file_out, "/");
if ($pos == -1) {
	substr($file_out, 0, 0, PRE_OUTFILE);
}else{
	substr($file_out, $pos + 1, 0, PRE_OUTFILE);
}

# ファイル出力
open(my $fh_out, "> " . $file_out) or die("Error:$!");
print $fh_out $output;
close($fh_out);


