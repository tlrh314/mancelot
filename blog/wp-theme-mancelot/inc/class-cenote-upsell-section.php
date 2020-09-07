<?php
/**
 * Class to render the Cenote Upsell Link.
 *
 * @package Cenote
 */

/**
 * Class to include upsell link campaign for theme.
 *
 * Class CENOTE_Upsell_Section
 */
class CENOTE_Upsell_Section extends WP_Customize_Section {
	/**
	 * Type of this section.
	 *
	 * @var string
	 */
	public $type = 'cenote-upsell-section';

	/**
	 * URL for this section.
	 *
	 * @var string
	 */
	public $url = '';

	/**
	 * Unique identifier.
	 *
	 * @var string
	 */
	public $id = '';

	/**
	 * Gather the parameters passed to client JavaScript via JSON.
	 *
	 * @return array The array to be exported to the client as JSON.
	 */
	public function json() {
		$json        = parent::json();
		$json['url'] = esc_url( $this->url );
		$json['id']  = $this->id;

		return $json;
	}

	/**
	 * An Underscore (JS) template for rendering this section.
	 */
	protected function render_template() {
		?>
		<li id="accordion-section-{{ data.id }}" class="cenote-upsell-accordion-section control-section-{{ data.type }} cannot-expand accordion-section">
			<h3 class="accordion-section-title"><a href="{{{ data.url }}}" target="_blank">{{ data.title }}</a></h3>
		</li>
		<?php
	}
}
