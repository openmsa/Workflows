##########################################################
#
# ���s���@    : perl nalconv_extension-info.pl [�t�@�C���p�X]
#               (��) perl nalconv_extension-info.pl /root/test.sql
#
# �d�l        : SQL����values�ɂ���JSON�`�����G�X�P�[�v����
#               ���s���ʂ͓��̓t�@�C���Ɠ����ꏊ�Ƀt�@�C����
#               �̍ŏ��� OUT_ ��t�����č쐬����
#
##########################################################

use strict;
use warnings;

# �萔
use constant DELI_F => "\"{";
use constant DELI_L => "}\"";
use constant DELI_VALIUES => "values";
use constant PRE_OUTFILE => "OUT_";

# �����̓��̓t�@�C���p�X���擾
my $file_in = shift;

open(my $fh_in, "< " . $file_in) or die("Error:$!");

# ���̓t�@�C���S�̂�ǂݍ���
my $content = do { local $/; <$fh_in> };

close($fh_in);

# �o�͗p������
my $output = "";

# SQL���́uvalues�v�܂ł͉��s�R�[�h���c��
my $wkText = $content;
my $pos = index($wkText, DELI_VALIUES);
if ($pos > 0) {
	$output = substr($wkText, 0, $pos);
	$output .= DELI_VALIUES . "\r\n";
	$wkText = substr($wkText, $pos + 6);
}

# ���s�R�[�h�ATAB�R�[�h���폜����
$wkText =~ s/\t//g;
$wkText =~ s/\r//g;
$wkText =~ s/\n//g;

# �ŏ��� "{ �� }" �̈ʒu���擾����
my $first = index($wkText, DELI_F);
my $last  = index($wkText, DELI_L);

# ��Ɨp������
my $tmpText = "";

while ($first > 0) {
	# ),( �̃J���}�̌��ɉ��s�R�[�h��}��
	$wkText =~ s/\)\,\(/\)\,\r\n\(/g;
	$output .= substr($wkText, 0, $first);
	$tmpText = substr($wkText, $first + 2, $last - $first - 2);
	$output .= DELI_F;

	# �_�u���N�H�[�e�[�V�����A�X���b�V�����G�X�P�[�v����
	$tmpText =~ s/\"/\\\\\"/g;
	$tmpText =~ s/\//\\\\\\\//g;

	$output .= $tmpText;
	$output .= DELI_L;
	$wkText = substr($wkText, $last + 2);

	# ���� "{ �� }" �̈ʒu���擾����
	$first = index($wkText, DELI_F);
	$last  = index($wkText, DELI_L);
}

# �Ō�̕������A������
$output .= $wkText;

# �o�̓t�@�C�����̐���
my $file_out = $file_in;
$pos = rindex($file_out, "/");
if ($pos == -1) {
	substr($file_out, 0, 0, PRE_OUTFILE);
}else{
	substr($file_out, $pos + 1, 0, PRE_OUTFILE);
}

# �t�@�C���o��
open(my $fh_out, "> " . $file_out) or die("Error:$!");
print $fh_out $output;
close($fh_out);

