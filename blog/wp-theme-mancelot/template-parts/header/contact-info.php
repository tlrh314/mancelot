<?php
/**
 * Header Info
 *
 * @package cenote
 */

$phone_number = get_theme_mod( 'cenote_header_contact_phone', '(123)456-7890' );
$email        = get_theme_mod( 'cenote_header_contact_email', 'example@domain.com' );
?>
<ul class="tg-contact-info">
	<li class="tg-contact-info__phone">
		<a href="tel:<?php echo esc_attr( $phone_number ); ?>">
			<i class="fa fa-phone"></i>
			<span><?php echo esc_html( $phone_number ); ?>
			</span>
		</a>
	</li>
	<li class="tg-contact-info__email">
		<a href="mailto:<?php echo esc_attr( $email ); ?>">
			<i class="fa fa-envelope"></i>
			<span><?php echo esc_html( $email ); ?></span>
		</a>
	</li>
</ul>
<!-- /.tg-contact-info -->
